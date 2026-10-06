"""Run syntax, shared-source, file-recovery and real PyTorch resume checks. No dataset training."""
import ast
import csv
import hashlib
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from prepare_notebooks import ROOT, SHARED, tagged, recipe_hash


def source(cell):
    return ''.join(cell['source'])


def definitions(code):
    tree = ast.parse(code)
    return '\n'.join(ast.get_source_segment(code, node) for node in tree.body
                     if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom)))


def main():
    notebooks = {p.name: json.loads(p.read_text()) for p in (ROOT / 'notebooks').glob('*.ipynb')}
    assert len(notebooks) == 4
    for name, notebook in notebooks.items():
        ids = [c['id'] for c in notebook['cells']]
        assert len(ids) == len(set(ids))
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                ast.parse(source(cell), filename=f"{name}:{cell['id']}")
                assert not cell['outputs'] and cell['execution_count'] is None
                assert 'from src' not in source(cell)
        cells = tagged(notebook)
        if 'recipe_fingerprint' in cells:
            assert recipe_hash(notebook) in source(cells['recipe_fingerprint'])
    primary = tagged(notebooks['03_crackfusion_train.ipynb'])
    mobile = tagged(notebooks['02_mobilevit_train.ipynb'])
    for tag in SHARED:
        assert primary[tag]['source'] == mobile[tag]['source'], tag
    assert primary['metrics']['source'] == tagged(notebooks['04_evaluation_and_comparison.ipynb'])['metrics']['source']
    print('Passed: four clean standalone notebooks, syntax, shared-source parity and recipe fingerprints.')

    # Exercise the actual audit extractor, including same-size corruption.
    audit = notebooks['01_data_audit.ipynb']
    scope = {'Path':Path,'json':json,'os':os,'ZipFile':ZipFile, '__name__':'check'}
    import shutil
    scope['shutil'] = shutil
    atomic_json = source(primary['atomic']).split('def save_checkpoint')[0]
    exec(atomic_json, scope)
    extraction = next(source(c) for c in audit['cells'] if c['cell_type']=='code' and 'def safe_extract' in source(c))
    exec(definitions(extraction), scope)
    with TemporaryDirectory() as scratch:
        root=Path(scratch); archive=root/'sample.zip'; target=root/'extracted'
        with ZipFile(archive,'w') as z:
            z.writestr('D/CD/a.jpg',b'complete-data')
        scope['safe_extract'](archive,target)
        original=(target/'D/CD/a.jpg').stat().st_mtime_ns
        scope['safe_extract'](archive,target)
        assert (target/'D/CD/a.jpg').stat().st_mtime_ns == original
        (target/'D/CD/a.jpg').write_bytes(b'corrupt--data')
        scope['safe_extract'](archive,target)
        assert (target/'D/CD/a.jpg').read_bytes()==b'complete-data'
        with ZipFile(root/'bad.zip','w') as z:
            z.writestr('../escape',b'bad')
        try: scope['safe_extract'](root/'bad.zip',target)
        except ValueError: pass
        else: raise AssertionError('Traversal accepted')
        class FakeTorch:
            def save(self,value,stream):
                stream.write(json.dumps(value).encode())
                if value.get('fail'): raise OSError('interrupted')
        scope['torch']=FakeTorch()
        exec(source(primary['atomic']),scope)
        checkpoint=root/'last.pt'
        scope['save_checkpoint'](checkpoint,{'epoch':1})
        try: scope['save_checkpoint'](checkpoint,{'epoch':2,'fail':True})
        except OSError: pass
        assert json.loads(checkpoint.read_bytes())=={'epoch':1}
    print('Passed: extraction reuse, same-size corruption repair, traversal rejection and atomic-write recovery.')

    # Two tiny synthetic epochs prove uninterrupted and interrupted/resumed runs agree.
    # MobileViT crosses its head/full boundary; official weights are checked separately in preflight.
    import torch
    from PIL import Image
    import numpy as np
    for name in ('03_crackfusion_train.ipynb','02_mobilevit_train.ipynb'):
        cells=tagged(notebooks[name]); ns={'__name__':'check'}
        exec(source(cells['environment']),ns)
        ns['DEVICE']=torch.device('cpu')
        if name.startswith('03'):
            exec(source(cells['model']),ns)
        else:
            exec(source(cells['model']).split('seed_everything(42)')[0],ns)
            net=ns['make_model'](pretrained=False)
            ns.update(DATA_CONFIG=ns['resolve_model_data_config'](net),
                      PARAMETERS=sum(p.numel() for p in net.parameters()),PRETRAINED=False,PRETRAINED_SHA256=None)
            del net
        for tag in ('atomic','data_helpers','transforms','metrics','evaluate','recipe_fingerprint','trainer'):
            exec(source(cells[tag]),ns)
        assert ns['binary_metrics']([0,1],[.1,.5])['accuracy']==1
        assert ns['binary_metrics']([0,1],[.1,.5],.7)['recall']==0
        with TemporaryDirectory() as scratch:
            root=Path(scratch); rows=[]; rng=np.random.default_rng(7)
            for split,count in [('train',4),('validation',2),('test',2)]:
                for i in range(count):
                    path=root/f'{split}_{i}.png'
                    Image.fromarray(rng.integers(0,256,(256,256,3),dtype=np.uint8)).save(path)
                    rows.append(dict(path=path.name,label=i%2,surface='deck',parent_id=f'{split}_{i}',
                        split=split,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
            manifest=root/'manifest.csv'
            with manifest.open('w',newline='') as stream:
                writer=csv.DictWriter(stream,fieldnames=rows[0]);writer.writeheader();writer.writerows(rows)
            ns.update(DATA_ROOT=root,MANIFEST=manifest,OUTPUT_ROOT=root/'continuous',PROTOCOL='source_separated',
                PARENT_ID_PROVENANCE='Synthetic fixture only',SEEDS=(42,),BATCH_SIZE=2,EFFECTIVE_BATCH=4,
                MAX_EPOCHS=2,HEAD_EPOCHS=1 if name.startswith('02') else 0,HEAD_LEARNING_RATE=1e-3,
                WARMUP_EPOCHS=1,MIN_EPOCHS=2,PATIENCE=15,LEARNING_RATE=1e-4,WEIGHT_DECAY=.01,
                THRESHOLD=.7,RUN_TEST=False)
            ns['run_experiment']()
            continuous=next(ns['OUTPUT_ROOT'].rglob('last_seed_42.pt'))
            expected=torch.load(continuous,map_location='cpu',weights_only=True)
            ns['OUTPUT_ROOT']=root/'resumed'; real_save=ns['save_json']
            def interrupt(path,value):
                real_save(path,value)
                if path.name=='history_seed_42.json' and len(value)==1:
                    raise KeyboardInterrupt('simulated runtime disconnect')
            ns['save_json']=interrupt
            try: ns['run_experiment']()
            except KeyboardInterrupt: pass
            else: raise AssertionError('Interruption was not reached')
            ns['save_json']=real_save
            ns['run_experiment']()
            last=next(ns['OUTPUT_ROOT'].rglob('last_seed_42.pt'))
            actual=torch.load(last,map_location='cpu',weights_only=True)
            assert actual['next_epoch']==2 and actual['history']==expected['history']
            for key,value in expected['model'].items():
                torch.testing.assert_close(actual['model'][key],value,rtol=0,atol=0)
            assert actual['phase']=='full'
            ns['run_experiment']()  # Completed seeds must validate, then reuse.
            # Hash validation must reject a modified audit image.
            Image.new('RGB',(256,256),'white').save(root/rows[0]['path'])
            try: ns['load_manifest'](manifest,root,'source_separated','Synthetic fixture only')
            except ValueError as error: assert 'audit hash' in str(error)
            else: raise AssertionError('Modified image accepted')
        print(f'Passed: {name} threshold consistency, finite optimization, exact epoch recovery, phase transition and completed-seed verification.')
    print('All checks passed. No development experiment was trained.')


if __name__ == '__main__':
    main()

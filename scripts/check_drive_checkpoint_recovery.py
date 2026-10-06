import ast,json,os,shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

n=json.load(open('notebooks/01_data_audit.ipynb'))
cell=lambda i: ''.join(n['cells'][i]['source'])
ns={'Path':Path,'json':json,'os':os,'shutil':shutil,'ZipFile':ZipFile}
exec(cell(2)[cell(2).index('def save_json'):],ns)
exec(cell(8)[:cell(8).index('# Always finish extraction')],ns)
with TemporaryDirectory() as directory:
 root=Path(directory); archive=root/'dataset.zip'; destination=root/'extracted'
 with ZipFile(archive,'w') as z:
  z.writestr('D/CD/a.jpg',b'complete-data')
  z.writestr('D/UD/b.jpg',b'other-data')
 ns['safe_extract'](archive,destination)
 original=(destination/'D/CD/a.jpg').stat().st_mtime_ns
 ns['safe_extract'](archive,destination)
 assert (destination/'D/CD/a.jpg').stat().st_mtime_ns==original
 (destination/'D/UD/b.jpg').write_bytes(b'partial')
 ns['safe_extract'](archive,destination)
 assert (destination/'D/UD/b.jpg').read_bytes()==b'other-data'
 bad=root/'bad.zip'
 with ZipFile(bad,'w') as z: z.writestr('../escape',b'no')
 try: ns['safe_extract'](bad,root/'unsafe')
 except ValueError: pass
 else: raise AssertionError('Unsafe archive accepted')
 progress=root/'progress.jsonl'
 progress.write_bytes(b'{"path":"complete"}\n{"path":"incomplete"')
 scope={'OUTPUT_DIR':root,'archive_sha256':'progress','json':json,'defaultdict':__import__('collections').defaultdict}
 # Execute the notebook's actual recovery block against an interrupted record.
 recovery=cell(12).split('all_paths =')[0].replace("('audit_progress_' + archive_sha256[:16] + '.jsonl')","'progress.jsonl'")
 exec(recovery,scope)
 assert scope['rows']==[{'path':'complete'}]
 assert progress.read_bytes()==b'{"path":"complete"}\n'
 print('Passed: extraction reuse, partial-file repair, traversal rejection, interrupted audit recovery.')

n=json.load(open('colab/03_crackfusion_tiny_checkpointed.ipynb'))
s=''.join(n['cells'][10]['source'])
with TemporaryDirectory() as directory:
 root=Path(directory)
 class FakeTorch:
  def save(self,value,stream):
   stream.write(json.dumps(value).encode())
   if value.get('fail'): raise OSError('simulated interruption')
 scope={'json':json,'os':os,'torch':FakeTorch()}
 exec(s[:s.index('def load_manifest')],scope)
 checkpoint=root/'last.pt'
 scope['save_checkpoint'](checkpoint,{'epoch':1})
 try: scope['save_checkpoint'](checkpoint,{'epoch':2,'fail':True})
 except OSError: pass
 assert json.loads(checkpoint.read_bytes())=={'epoch':1}
 print('Passed: interrupted checkpoint write preserves the previous checkpoint.')
for path in ['notebooks/01_data_audit.ipynb','colab/03_crackfusion_tiny_checkpointed.ipynb']:
 for i,c in enumerate(json.load(open(path))['cells']):
  if c['cell_type']=='code': ast.parse(''.join(c['source']),filename=f'{path}:{i}')
print('All notebook code cells parse. Full training resume needs a PyTorch runtime.')

# Exercise the trainer's actual bundle setup without requiring a GPU or PyTorch.
import csv,hashlib,io
from PIL import Image
n=json.load(open('colab/03_crackfusion_tiny_checkpointed.ipynb'))
setup=''.join(n['cells'][9]['source']).split('\nif DRIVE_DATA_DIR:')[0]
with TemporaryDirectory() as temporary:
 root=Path(temporary); base=root/'drive'; base.mkdir(); cache=root/'content'
 scope={'Path':Path,'ZipFile':ZipFile,'csv':csv,'json':json,'shutil':shutil,'hashlib':hashlib}
 exec(setup.replace('/content/crackfusion_data',str(cache)).replace('/content/crackfusion_colab_bundle.zip',str(root/'upload.zip')),scope)
 try: scope['prepare_colab_data'](base)
 except FileNotFoundError: pass
 else: raise AssertionError('Missing audit accepted')
 columns=['path','label','surface','parent_id','split','sha256','split_basis']
 rows=[dict(zip(columns,[f'D/CD/{i}.png',str(i%2),'deck','','dev_train' if i<2880 else 'dev_validation','abc','tile_development_only'])) for i in range(3600)]
 manifest=io.StringIO(); writer=csv.DictWriter(manifest,fieldnames=columns); writer.writeheader(); writer.writerows(rows)
 bundle=base/'crackfusion_colab_bundle.zip'
 with ZipFile(bundle,'w') as z:
  z.writestr('development_manifest.csv',manifest.getvalue()); z.writestr('dataset/SDNET2018/D/CD/0.png',b'image')
 data,path=scope['prepare_colab_data'](base)
 assert path.read_text()==manifest.getvalue().replace('\r\n','\n')
 assert (data/'D/CD/0.png').read_bytes()==b'image'
 scope['prepare_colab_data'](base)
 with ZipFile(bundle,'w') as z: z.writestr('../escape',b'bad')
 try: scope['prepare_colab_data'](base)
 except ValueError: pass
 else: raise AssertionError('Unsafe bundle accepted')
 # Validate audit split aliases and content-hash enforcement against real images.
 source=''.join(n['cells'][10]['source']); function=source[source.index('def load_manifest'):source.index('class CrackDataset')]
 scope['Image']=Image; exec(function,scope)
 rows=[]
 for i,split in enumerate(('dev_train','dev_train','dev_validation','dev_validation')):
  image=root/f'{i}.png'; Image.new('RGB',(256,256),(i*50,20,30)).save(image)
  rows.append(dict(zip(columns,[image.name,str(i%2),'deck','',split,hashlib.sha256(image.read_bytes()).hexdigest(),'tile_development_only'])))
 path=root/'manifest.csv'
 with path.open('w',newline='') as stream:
  writer=csv.DictWriter(stream,fieldnames=columns); writer.writeheader(); writer.writerows(rows)
 groups=scope['load_manifest'](path,root,'development'); assert len(groups['train'])==len(groups['validation'])==2
 Image.new('RGB',(256,256),'white').save(root/'0.png')
 try: scope['load_manifest'](path,root,'development')
 except ValueError as error: assert 'audit hash' in str(error)
 else: raise AssertionError('Changed audit image accepted')
model=Path('src/crackfusion_tiny.py').read_text().split('def _smoke_test')[0]
assert ''.join(n['cells'][3]['source']).startswith(model)
all_code='\n'.join(''.join(c['source']) for c in n['cells'] if c['cell_type']=='code')
assert 'from src' not in all_code and 'git", "clone' not in all_code
print('Passed: standalone model parity, missing export rejection, bundle caching, traversal rejection, audit aliases and changed-image rejection.')

# Check AMP overflow control flow using the notebook's actual helper.
from types import SimpleNamespace
code=''.join(n['cells'][12]['source']) if 'step_optimizer' in ''.join(n['cells'][12]['source']) else ''.join(json.load(open('colab/03_crackfusion_tiny_checkpointed.ipynb'))['cells'][12]['source'])
helper=code[:code.index('def train_one_seed')]
class Flag:
 def __init__(self,value): self.value=value
 def all(self): return self
 def item(self): return self.value
class FakeScaler:
 def __init__(self,enabled): self.enabled=enabled; self.overflow=False; self.scale=8
 def unscale_(self,opt): self.overflow=not opt.finite
 def is_enabled(self): return self.enabled
 def step(self,opt):
  if not self.overflow: opt.steps+=1
 def update(self):
  if self.overflow: self.scale/=2
class FakeOptimizer:
 def __init__(self,finite): self.finite=finite; self.steps=0; self.cleared=False
 def zero_grad(self,**kwargs): self.cleared=True
for finite,enabled in [(True,True),(False,True),(False,False)]:
 calls=[]; opt=FakeOptimizer(finite); scaler=FakeScaler(enabled)
 net=SimpleNamespace(parameters=lambda:[SimpleNamespace(grad=finite)])
 scope={'torch':SimpleNamespace(isfinite=lambda g:Flag(g),stack=lambda values:Flag(all(v.value for v in values))),
        'nn':SimpleNamespace(utils=SimpleNamespace(clip_grad_norm_=lambda *a,**k:calls.append('clip')))}
 exec(helper,scope)
 if not finite and not enabled:
  try: scope['step_optimizer'](net,opt,scaler)
  except FloatingPointError: pass
  else: raise AssertionError('Unscaled nonfinite gradient accepted')
 else:
  assert scope['step_optimizer'](net,opt,scaler)==finite
  assert opt.steps==int(finite) and opt.cleared
  assert calls==(['clip'] if finite else [])
  assert scaler.scale==(8 if finite else 4)
print('Passed: finite-gradient clipping, AMP overflow skips update and lowers scale, non-AMP failure retained.')

local=json.load(open('notebooks/03_crackfusion_tiny.ipynb'))
colab=json.load(open('colab/03_crackfusion_tiny_checkpointed.ipynb'))
for i in (5,7,10,12,14,16,18):
 assert local['cells'][i]['source']==colab['cells'][i]['source'], f'Training code drift in cell {i}'
for path in Path('colab').glob('*.ipynb'):
 for i,cell in enumerate(json.loads(path.read_text())['cells']):
  if cell['cell_type']=='code':
   ast.parse(''.join(cell['source']),filename=f'{path}:{i}')
   assert not cell['outputs'] and cell['execution_count'] is None
print('Passed: local/Colab training parity and clean, parseable Colab notebooks.')

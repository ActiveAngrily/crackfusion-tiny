"""Propagate tagged shared cells from notebook 03 and fingerprint runnable recipes."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / 'notebooks'
SHARED = ('environment', 'bundle', 'atomic', 'data_helpers', 'metrics', 'evaluate', 'trainer', 'preflight')


def tagged(notebook):
    result = {}
    for cell in notebook['cells']:
        for tag in cell.get('metadata', {}).get('tags', []):
            if tag in result:
                raise ValueError(f'Duplicate cell tag: {tag}')
            result[tag] = cell
    return result


def recipe_hash(notebook):
    cells = tagged(notebook)
    # Configuration values are hashed separately by run_experiment; Markdown is excluded.
    tags = ('environment', 'model', 'bundle', 'atomic', 'data_helpers', 'transforms', 'metrics', 'evaluate', 'trainer')
    return hashlib.sha256(''.join(''.join(cells[tag]['source']) for tag in tags).encode()).hexdigest()


def prepare():
    notebooks = {p.name: json.loads(p.read_text()) for p in NOTEBOOKS.glob('*.ipynb')}
    primary = tagged(notebooks['03_crackfusion_train.ipynb'])
    mobile = tagged(notebooks['02_mobilevit_train.ipynb'])
    for tag in SHARED:
        mobile[tag]['source'] = primary[tag]['source'].copy()
        mobile[tag]['metadata']['generated_from'] = f'03_crackfusion_train.ipynb#{tag}'
    evaluation = tagged(notebooks['04_evaluation_and_comparison.ipynb'])
    evaluation['metrics']['source'] = primary['metrics']['source'].copy()
    evaluation['metrics']['metadata']['generated_from'] = '03_crackfusion_train.ipynb#metrics'
    for name, notebook in notebooks.items():
        cells = tagged(notebook)
        if 'recipe_fingerprint' in cells:
            cells['recipe_fingerprint']['source'] = [f"TRAINING_SOURCE_SHA256 = '{recipe_hash(notebook)}'\n"]
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                cell['execution_count'], cell['outputs'] = None, []
        notebook['metadata'].setdefault('colab', {})['name'] = name
        (NOTEBOOKS / name).write_text(json.dumps(notebook, indent=1) + '\n')
    print('Prepared four standalone notebooks; shared cells synchronized and recipes fingerprinted.')


if __name__ == '__main__':
    prepare()

"""Keep local and standalone Colab entry points consistent. Run from any directory."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads((ROOT / path).read_text())

def source(notebook, index):
    return ''.join(notebook['cells'][index]['source'])

def replace(notebook, index, text):
    notebook['cells'][index]['source'] = text.splitlines(keepends=True)

def write(path, notebook):
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            cell['outputs'], cell['execution_count'] = [], None
    (ROOT / path).write_text(json.dumps(notebook, indent=1) + '\n')

# Model source is authoritative in src; the Colab copy embeds it for standalone use.
training = read('colab/03_crackfusion_tiny_checkpointed.ipynb')
model = (ROOT / 'src/crackfusion_tiny.py').read_text().split('def _smoke_test')[0]
replace(training, 3, model + '\n' + source(training, 3)[source(training, 3).index('model = CrackFusionTiny()'):])
import re
replace(training, 12, re.sub(r"model_source_sha256='[a-f0-9]+'", "model_source_sha256='" + hashlib.sha256(model.encode()).hexdigest() + "'", source(training, 12)))
write('colab/03_crackfusion_tiny_checkpointed.ipynb', training)

# Training/data/checkpoint functions are identical; only environment and model loading differ.
local = json.loads(json.dumps(training))
setup = source(local, 1)
start, end = setup.index('DRIVE_DATA_DIR = None'), setup.index('RUN_SOFTWARE_CHECKS =')
replace(local, 1, setup[:start] + '''PROJECT_ROOT = next(p for p in (Path.cwd(), *Path.cwd().parents) if (p / "src" / "crackfusion_tiny.py").is_file())
sys.path.insert(0, str(PROJECT_ROOT))

''' + setup[end:])
replace(local, 3, 'from src.crackfusion_tiny import CrackFusionTiny, count_parameters\n\n' + source(local, 3)[source(local, 3).index('model = CrackFusionTiny()'):])
config = source(local, 9)
replace(local, 9, '''DATA_ROOT = PROJECT_ROOT / "dataset" / "SDNET2018" / "SDNET2018"
MANIFEST = PROJECT_ROOT / "outputs" / "data_audit" / "development_manifest.csv"
OUTPUT_ROOT = PROJECT_ROOT / "outputs" / "crackfusion_tiny"
PROTOCOL = "development"
RUN_TRAINING = False  # Enable when local GPU training is intended.
''' + config[config.index('PARENT_ID_PROVENANCE ='):])
replace(local, 0, '''# CrackFusion-Tiny — local model development

Run from this repository after installing `requirements.txt`. The model is loaded from `src/crackfusion_tiny.py`. Run notebook 01 first to prepare the audit manifest. Set `RUN_TRAINING=True` in section 6 for local training, or use `colab/03_crackfusion_tiny_checkpointed.ipynb` for the standalone Drive workflow.

This uses the 3,600-image development subset: 2,880 training and 720 validation images. Results retain `tile_development_only`. Outputs and resumable epoch checkpoints are saved to `outputs/crackfusion_tiny`. Optional synthetic checks are disabled by default.

## 2. Environment
''')
local['metadata'].get('colab', {}).pop('name', None)
write('notebooks/03_crackfusion_tiny.ipynb', local)

# Local audit code is authoritative; Colab uses the same cells with Drive paths.
audit = read('notebooks/01_data_audit.ipynb')
setup = source(audit, 2)
start, end = setup.index('WORK_DIR ='), setup.index('OFFICIAL_RECORD_URL =')
replace(audit, 2, setup[:start] + '''from google.colab import drive
if not Path("/content/drive/MyDrive").is_dir():
    drive.mount("/content/drive")
PROJECT_ROOT = Path("/content/drive/MyDrive/Fridge/major_project_dataset")
DATA_DIR = PROJECT_ROOT
ARCHIVE_PATH = DATA_DIR / "DATA_Maguire_20180517_ALL.zip"
EXTRACT_DIR = DATA_DIR / "SDNET2018"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "data_audit"

''' + setup[end:])
replace(audit, 23, '''## Outputs and training handoff

Audit reports and `crackfusion_colab_bundle.zip` are saved under `MyDrive/Fridge/major_project_dataset/outputs/data_audit`. Notebook 03 loads that bundle automatically. Running the local audit and uploading its finished bundle is faster than extracting thousands of files in Drive.

The 3,600-image split is `tile_development_only`; verified parent mapping and final evaluation remain pending.
''')
audit['metadata'].setdefault('colab', {})['name'] = '01_data_audit_checkpointed.ipynb'
write('colab/01_data_audit_checkpointed.ipynb', audit)
write('colab/04_crackfusion_evaluation.ipynb', read('colab/04_crackfusion_evaluation.ipynb'))
print('Synced model, audit and training entry points; cleared notebook outputs for Git.')

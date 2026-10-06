# CrackFusion-Tiny

CrackFusion-Tiny is a compact CNN–Transformer study for binary concrete-crack
classification. The project compares a pretrained MobileViT-XS reference with a
custom model that exposes separate local-convolution and global-attention branches.

The primary dataset is SDNET2018. Current development experiments use a preliminary
tile-level development split and may contain parent-photograph leakage. They are
pipeline checks, not research-valid test results.

## Repository structure

```text
docs/          Literature review, experimental protocol, and methodology
notebooks/     Data preparation, baselines, model development, and analysis
colab/         Standalone audit and checkpointed training for Google Colab
scripts/       Notebook synchronization, recovery checks, and document generation
sources/       Literature metadata snapshot
src/           Importable CrackFusion-Tiny model
dataset/       Local dataset files; ignored by Git
outputs/       Generated checkpoints, metrics, and figures; ignored by Git
```

## Setup

```bash
python -m pip install -r requirements.txt
```

Obtain SDNET2018 from the
[official dataset record](https://digitalcommons.usu.edu/all_datasets/48/).
Dataset archives and extracted images are intentionally excluded from Git.

Run notebooks from the repository root:

1. [Data audit and manifest](notebooks/01_data_audit.ipynb)
2. [MobileViT-XS baseline](notebooks/02_mobilevit_baseline.ipynb)
3. [CrackFusion-Tiny implementation](notebooks/03_crackfusion_tiny.ipynb)
4. [Evaluation and analysis](notebooks/04_evaluation_and_analysis.ipynb)

## Colab and Drive workflow

The standalone notebooks below match the maintained Drive entry points:

| Repository notebook | Drive notebook | Purpose |
|---|---|---|
| [colab/01_data_audit_checkpointed.ipynb](colab/01_data_audit_checkpointed.ipynb) | [Audit in Colab](https://colab.research.google.com/drive/1qrQCrFlZKvlNA9SlGZhm8fH12gjbpDf0) | Audit SDNET2018 and export the development bundle |
| [colab/03_crackfusion_tiny_checkpointed.ipynb](colab/03_crackfusion_tiny_checkpointed.ipynb) | [Training in Colab](https://colab.research.google.com/drive/1xFijJCpZnLH5HElEEVM0eFk8EQCIUgTj) | Load the bundle and train with resumable epoch checkpoints |

For the faster workflow, run the local audit in `notebooks/01_data_audit.ipynb`,
upload `outputs/data_audit/crackfusion_colab_bundle.zip` to the Drive dataset
folder, and run the Colab training notebook on a T4 GPU. The bundle contains
3,600 development images (2,880 train / 720 validation), not the full dataset.

Drive's `Fridge/major_project_dataset` contains:

```text
colab/                         The two maintained notebook entry points
DATA_Maguire_20180517_ALL.zip    Original dataset archive for reproducibility
SDNET2018/                     Extracted dataset, original readme, and extraction state
crackfusion_colab_bundle.zip    Bundle consumed by the current training run
outputs/data_audit/             Audit evidence and portable manifests
outputs/crackfusion_tiny/       Run configurations, checkpoints, predictions and metrics
```

Keep dataset and output paths unchanged while a run is active. Colab file IDs
stay stable when notebooks are moved into the `colab` folder.

### Maintaining notebook consistency

Edit model code in `src/crackfusion_tiny.py`, audit code in the local audit
notebook, and training logic in the Colab training notebook. Then run:

```bash
python scripts/sync_notebooks.py
python scripts/check_drive_checkpoint_recovery.py
```

The sync command embeds the same model in Colab, regenerates the local training
entry point and the Colab audit entry point, and strips execution outputs from
Git copies. Upload changed Colab copies into their existing Drive files; do this
between runs. Saved runtime outputs may differ, but code cells should match.
The recovery check covers file safety, audit hashes, AMP recovery control flow,
and local/Colab code parity; full CUDA behavior needs a live training runtime.

## Research status

- Literature review and methodology are complete.
- The custom CrackFusion-Tiny graph is implemented and software-validated.
- The prescribed architecture has 284,337 trainable parameters (0.284M); this
  measured count supersedes the earlier 1–3M planning estimate.
- Verified parent-photo mapping, source-separated training, matched baselines, and
  cross-surface evaluation remain pending.

Synthetic learning checks establish that the code can optimize; they do not measure
crack-classification accuracy.

## Documentation

- [Literature review](docs/literature_review.md)
- [Experimental protocol](docs/experimental_protocol.md)
- [Methodology](docs/methodology.pdf)

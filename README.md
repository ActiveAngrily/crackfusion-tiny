# CrackFusion-Tiny

Compact CNN–Transformer concrete-crack classification using SDNET2018. The implemented
model has **284,337 parameters**; pretrained MobileViT-XS is the practical reference.
Current experiments use **3,600 development tiles (2,880 train / 720 validation)**.
Parent-photo separation is unverified. Completed three-seed CrackFusion run
`run_4d1bf234e5ee01bc` is preserved.

## One workflow, locally or in Colab

| Notebook | Purpose | Drive copy |
|---|---|---|
| [01 — Data audit](notebooks/01_data_audit.ipynb) | Local/Colab audit and portable bundle | [Open](https://colab.research.google.com/drive/1qrQCrFlZKvlNA9SlGZhm8fH12gjbpDf0) |
| [02 — MobileViT training](notebooks/02_mobilevit_train.ipynb) | Pretrained reference, preflight and resumable training | [Open](https://colab.research.google.com/drive/1DxxT13Ckrv1XK8ZYzXAAZvkcDa6ic9Rk) |
| [03 — CrackFusion training](notebooks/03_crackfusion_train.ipynb) | Standalone model, preflight and resumable training | [Open](https://colab.research.google.com/drive/1xFijJCpZnLH5HElEEVM0eFk8EQCIUgTj) |
| [04 — Evaluation and comparison](notebooks/04_evaluation_and_comparison.ipynb) | Either model, paired predictions, figures, optional architecture inspection | [Open](https://colab.research.google.com/drive/1i4N6zCukGXFTKBGnr0aLTaANejmOAecM) |

All notebooks contain their runtime code; Colab needs no clone or `src/` import.
Select T4 for training and CPU for evaluation. Both trainers default to
`RUN_TRAINING=False`: run preparation checks, then enable training explicitly.
MobileViT uses five head epochs and up to 50 fine-tuning epochs for each of three
seeds, with early stopping; CrackFusion uses up to 100 epochs per seed.

For local use:

```bash
python -m pip install -r requirements.txt
```

The notebooks find the repository from its root or `notebooks/`. Put the official
archive at `dataset/DATA_Maguire_20180517_ALL.zip`; the audit locates the extracted
six folders. Obtain data from the [official SDNET2018 record](https://digitalcommons.usu.edu/all_datasets/48/).

After local auditing, upload `outputs/data_audit/crackfusion_colab_bundle.zip` to
`MyDrive/Fridge/major_project_dataset`, and retain accompanying audit evidence under
`outputs/data_audit` there. Trainers cache images on Colab disk and verify all their
hashes. Dataset paths and completed output folders stay stable.

## Repository layout

```text
notebooks/             Four primary standalone local/Colab notebooks
docs/literature/       Synthesis, evidence and reference metadata
docs/planning/         Protocol, methodology PDF and codebase audit
scripts/              Notebook preparation, checks and PDF generation
dataset/              Local data; ignored by Git
outputs/              Audit, runs, reports and migration snapshot; ignored by Git
```

Drive retains `Fridge/major_project_dataset/colab` and existing notebook IDs. Results
save beside the dataset under `outputs/crackfusion_tiny` or `outputs/mobilevit_baseline`.
Notebook 04 exports into each run's `evaluation/`. Set its explicit `MOBILEVIT_RUN_NAME`
after training to export paired comparisons. Checkpoints, histories, random states,
predictions and metrics save atomically; recovery restarts any incomplete epoch.

## Maintaining notebooks

Edit the model and shared cells in **notebook 03**. Edit model-specific MobileViT
configuration/transforms in notebook 02 and audit logic in notebook 01. Stable tags
identify generated cells; preparation fingerprints runnable training recipes.

```bash
python scripts/prepare_notebooks.py
python scripts/check_notebooks.py
python scripts/build_methodology.py
```

Checks use small synthetic data for exact epoch recovery, the MobileViT head/full
transition, threshold consistency, file safety and source parity. Update existing
Drive notebook IDs between runs. Historical runs retain their provenance; changed
recipes create separate folders.

## Research documents

- [Literature review](docs/literature/README.md)
- [Experimental protocol](docs/planning/experimental_protocol.md)
- [Methodology](docs/planning/methodology.pdf)
- [Codebase audit and resolution](docs/planning/codebase_audit.md)

Parent mapping, grouped final splits, matched baselines, ablations, held-out-surface
tests and publication profiling remain pending. Current validation results and seed
spread do not establish generalization to unseen photographs.

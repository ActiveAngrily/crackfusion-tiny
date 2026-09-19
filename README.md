# CrackFusion-Tiny

A compact CNN–Transformer research project for concrete-crack image classification.

The project uses a pretrained MobileViT-XS baseline as the first implementation step, then investigates an explicit local-convolution/global-attention fusion model under source-aware evaluation. The primary dataset is SDNET2018.

## Status

- Stages 1–5: MobileViT smoke test, SDNET2018 audit, development training, presentation artifacts, and architecture inspection notebooks.
- Phase 3: methodology PDF for the proposed CrackFusion-Tiny study.
- Custom model: [`notebooks/06_crackfusion_tiny_implementation.ipynb`](notebooks/06_crackfusion_tiny_implementation.ipynb) contains the complete scratch-trained architecture, executable software checks, and opt-in manifest-based training/evaluation.
- Research-valid parent-photo mapping and source-separated evaluation: still pending.

Results from the current development split are pipeline-validation results only and must not be presented as source-separated research results.

## Run order

Run the notebooks in numerical order:

1. [`notebooks/01_mobilevit_smoke_test.ipynb`](notebooks/01_mobilevit_smoke_test.ipynb)
2. [`notebooks/02_sdnet2018_audit_manifest.ipynb`](notebooks/02_sdnet2018_audit_manifest.ipynb)
3. [`notebooks/03_mobilevit_development_training.ipynb`](notebooks/03_mobilevit_development_training.ipynb)
4. [`notebooks/04_mobilevit_presentation_artifacts.ipynb`](notebooks/04_mobilevit_presentation_artifacts.ipynb)
5. [`notebooks/05_mobilevit_architecture_inspection.ipynb`](notebooks/05_mobilevit_architecture_inspection.ipynb)
6. [`notebooks/06_crackfusion_tiny_implementation.ipynb`](notebooks/06_crackfusion_tiny_implementation.ipynb) — standalone custom model; run all cells for software validation without a dataset. Set dataset paths, parent-ID provenance, and `RUN_TRAINING` for real training. `RUN_TEST` defaults to false.

The two combined Colab exports are in [`notebooks/colab/`](notebooks/colab/). Run notebooks from the repository root so their relative `outputs/` paths remain consistent.

The custom notebook follows the Phase 3 tensor widths and has **284,337 trainable parameters (0.284M)**, superseding the preliminary 1–3M estimate. Synthetic checks are not crack-classification results. Full source-separated training and baseline comparisons remain pending. The notebook is self-contained; `scripts/build_crackfusion_notebook.py` regenerates it (and clears saved execution outputs).

The notebooks download or consume SDNET2018 locally. The dataset is intentionally not included in this repository; obtain it from the [official dataset record](https://digitalcommons.usu.edu/all_datasets/48/).

The methodology PDF is at [`docs/phase3_crackfusion_methodology.pdf`](docs/phase3_crackfusion_methodology.pdf). Project decisions and handoff notes are in [`docs/project_handoff.md`](docs/project_handoff.md) and [`docs/mobilevit_build_plan.md`](docs/mobilevit_build_plan.md).

## Repository layout

- `notebooks/` — numbered implementation and analysis notebooks.
- `notebooks/colab/` — combined convenience exports.
- `docs/` — research synthesis, methodology, plans, and handoff notes.
- `scripts/` — reproducible document and notebook builders.
- `sources/` — literature metadata.
- `dataset/` — local, ignored SDNET2018 files.
- `outputs/` — local, ignored experiment results.

## Scope

This repository contains research notebooks, planning documents, literature metadata, and the methodology artifact. It is not yet a packaged training library or deployment service.

# CrackFusion-Tiny

A compact CNN–Transformer research project for concrete-crack image classification.

The project uses a pretrained MobileViT-XS baseline as the first implementation step, then investigates an explicit local-convolution/global-attention fusion model under source-aware evaluation. The primary dataset is SDNET2018.

## Status

- Stages 1–5: MobileViT smoke test, SDNET2018 audit, development training, presentation artifacts, and architecture inspection notebooks.
- Phase 3: methodology PDF for the proposed CrackFusion-Tiny study.
- Research-valid parent-photo mapping and source-separated evaluation: still pending.

Results from the current development split are pipeline-validation results only and must not be presented as source-separated research results.

## Run order

Run the notebooks in numerical order:

1. `01_mobilevit_smoke_test.ipynb`
2. `02_sdnet2018_audit_manifest.ipynb`
3. `03_mobilevit_development_training.ipynb`
4. `04_mobilevit_presentation_artifacts.ipynb`
5. `05_mobilevit_architecture_inspection.ipynb`

The notebooks download or consume SDNET2018 locally. The dataset is intentionally not included in this repository; obtain it from the [official dataset record](https://digitalcommons.usu.edu/all_datasets/48/).

The methodology PDF is at [`output/pdf/phase3_crackfusion_methodology.pdf`](output/pdf/phase3_crackfusion_methodology.pdf). Project decisions and handoff notes are in [`checkout.md`](checkout.md) and [`mobilevit_build_plan.md`](mobilevit_build_plan.md).

## Scope

This repository contains research notebooks, planning documents, literature metadata, and the methodology artifact. It is not yet a packaged training library or deployment service.

# CrackFusion-Tiny

CrackFusion-Tiny is a compact CNN–Transformer study for binary concrete-crack
classification. The project compares a pretrained MobileViT-XS reference with a
custom model that exposes separate local-convolution and global-attention branches.

The primary dataset is SDNET2018. Current MobileViT measurements use a preliminary
tile-level development split and may contain parent-photograph leakage. They are
pipeline checks, not research-valid test results.

## Repository structure

```text
docs/          Literature review, experimental protocol, and methodology
notebooks/     Data preparation, baselines, model development, and analysis
scripts/       Reproducible document generation
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

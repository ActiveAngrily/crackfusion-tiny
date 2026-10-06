# Experimental protocol

This file governs current experiments. Historical literature notes retain earlier
proposals; the generated methodology follows this protocol.

## Research question

Under source-separated and cross-surface evaluation, does one explicit fusion of
lightweight local CNN features and global Transformer features improve concrete-crack
classification over parameter-matched single-family baselines?

## Current development stage

The audit contains 56,092 SDNET2018 tiles, with 13 duplicate copies excluded. The
portable development bundle contains 3,600 balanced tiles: 2,880 train and 720
validation, sampled as 600 per class/surface folder. Its manifest SHA-256 is
`c556b503912fbbc6427b2a173076bb1eee76892ea675f6da62ce8465eba3a6d7`.
A complete verified tile-to-parent mapping remains unavailable. Results retain
`tile_development_only`; validation-selected scores are preliminary.

CrackFusion run `run_4d1bf234e5ee01bc` completed all three seeds and remains unchanged.
Updated recipes use separate run identities containing training-code fingerprints.
MobileViT uses the same development manifest and seed set. Its binary classifier
has 1,933,233 parameters with timm 1.0.20, compared with CrackFusion's 284,337.

| Setting | CrackFusion-Tiny development | MobileViT-XS development |
|---|---|---|
| Initialization | Scratch | Official `mobilevit_xs.cvnets_in1k` ImageNet weights |
| Input | 224×224 RGB | Official checkpoint configuration, 256×256 RGB |
| Normalization | Training-only mean/std | Official checkpoint mean/std |
| Augmentation | Crop .85–1, H/V flips, rotation ±15°, brightness/contrast ±15% | Same strength, official resolution/interpolation |
| Seeds | 42, 1337, 2026 | Same |
| Micro/effective batch | 16 / 64 | Same |
| Optimizer/loss | AdamW, weight decay .01, training-only positive-weight BCE | Same |
| Schedule | LR 3e-4, 5 warm-up epochs, cosine, max 100 | 5 head epochs at 1e-3; max 50 full epochs at 1e-4 with 5 full-phase warm-up epochs and cosine |
| Selection | Best validation macro-F1 | Same |
| Early stopping | Patience 15 after minimum 30 total epochs | Same; stale counter resets at phase transition |
| Threshold | .5 | Same |

During head training the MobileViT backbone, including BatchNorm, stays in evaluation
mode. Full fine-tuning unfreezes all parameters. Its size, initialization, preprocessing
and epoch budget differ from CrackFusion; it is a practical transfer reference.

## Final study data

SDNET2018 tiles derive from 230 photographs. Document a verified parent mapping,
exclude corrupt images and duplicate copies, then freeze a group-stratified 70/15/15
train/validation/test manifest. Every parent's tiles stay in one partition. Group
separation has priority over exact proportions. Preserve natural validation/test
prevalence. Validation controls selection and secondary thresholds; open test data
only after those choices are fixed. A full-data tile-random run cannot substitute
for source-separated evaluation.

## Models and ablations

CrackFusion-Tiny has **284,337 parameters**, fixed 224×224 input, a shared CNN stem,
parallel local/global branches, a 14×14 grid of width-96 tokens, two four-head
pre-normalized Transformer encoders and one concat-plus-1×1 fusion producing a logit.
The implemented graph has no extra local projection or stochastic-depth operator.

| ID | Experiment | Role |
|---|---|---|
| B0 | Pretrained MobileViT-XS | Practical transfer reference, reported separately |
| B1 | Parameter-matched CNN-only | Local-family baseline |
| B2 | Parameter-matched raw-patch Transformer-only | Global-family baseline |
| B3 | Parameter-matched serial CNN→Transformer | Serial hybrid baseline |
| H1 | CrackFusion-Tiny | Primary parallel-fusion model |
| A1 | H1 with global branch removed | Global contribution; separately report unexpanded branch-removal model |
| A2 | H1 with local branch removed | Local contribution; separately report unexpanded branch-removal model |
| A3 | H1 versus B3 | Parallel versus serial; reuse B3 without another run |
| A4 | Adaptive gate versus concat | Optional extension after core comparisons |

Matched B1–B3 target within ±10% of H1's parameters and share scratch initialization,
224×224 input, manifests, augmentation, weighted BCE, effective batch, optimizer
budget and seeds. Branch-removal ablations are not automatically parameter matched;
report actual counts. Width/depth and any equal-budget search are fixed before test
access. Attention depth, token-grid, fixed-filter and extra transfer sweeps are optional.

## Evaluation

Report every seed and mean/sample seed standard deviation for macro-F1, crack F1,
recall, balanced accuracy and **average precision** (`average_precision_score`, not
trapezoidal PR-AUC). Also include accuracy, precision, specificity, ROC-AUC, confusion
matrices, per-surface metrics, parameters and measured efficiency.

Three rotations train on two surfaces and test on the untouched third: deck, wall,
pavement. Validation uses grouped photos from training surfaces. Never tune on the
held-out surface. This tests composite domain shift. Final uncertainty uses paired
parent-photograph bootstrap resampling; correlated tiles are not independent, and
seed spread is not a confidence interval. Measure latency/memory on the same device
and record resolution, batch, precision, threads and timing boundaries. Short optional
notebook timing checks are software diagnostics, not publication profiling.

## Artifact and recovery contract

Both trainers save configurations, manifest and training-code hashes, model provenance,
best weights, last epoch, phase, optimizer, AMP scaler, history, loader state and
Python/NumPy/Torch/CUDA random states. Predictions and metrics use one schema.
Completed seeds are verified before reuse; atomic writes preserve the preceding
checkpoint on failure. Interrupted epochs restart from the last completed epoch.

Notebook 04 evaluates either model or paired results on identical audited images.
Final study claims await parent mapping, grouped splits, matched baselines, ablations,
held-out-surface tests, uncertainty and efficiency measurement. Current results do
not establish structural diagnosis, physical crack width or segmentation performance.

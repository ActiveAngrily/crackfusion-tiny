> Historical audit: filenames below describe the repository before consolidation. Current resolution status is at the end.

# Codebase and comparison readiness audit

Date: 6 October 2026. Repository revision: `0ca33b7`.

## Decision

**Hold MobileViT training until its notebook is prepared and checked.** The
completed CrackFusion development run passes the artifact and data checks below.
The existing MobileViT notebook cannot provide the planned three-seed, resumable
Drive comparison without changes. Training was not started during this audit.

This is a correctness, reproducibility and plan-alignment audit. It does not
certify that every possible runtime failure is absent or revalidate every cited
research paper. No training logic, saved checkpoints or Drive notebooks were
changed during the audit.

## Scope and checks

Reviewed all seven notebooks, `src/crackfusion_tiny.py`, all three scripts,
requirements, README, experimental protocol, methodology generator and relevant
literature-review experiment sections. Checked the bibliography snapshot's cited
keys. Compared the three maintained Drive notebooks with their repository copies.

- All Python scripts, the model module and all notebook code cells parse.
- `python3 scripts/check_drive_checkpoint_recovery.py` passes: extraction/recovery,
  path traversal, interrupted checkpoint preservation, changed-image rejection,
  AMP overflow control flow, model/training parity and metric definitions.
- Drive audit and evaluation cell sources match the repository. Drive training
  contains one additional two-line Drive-mount cell; all remaining code matches.
  This extra cell is redundant and does not change the model or training recipe.
- The saved model-source hash matches `src/crackfusion_tiny.py`; the saved run ID
  recomputes to `4d1bf234e5ee01bc` from its original configuration.
- The local audit manifest, training run manifest and bundle manifest match
  byte-for-byte: SHA-256
  `c556b503912fbbc6427b2a173076bb1eee76892ea675f6da62ce8465eba3a6d7`.
- All 3,600 selected local images match their audit SHA-256 values, their bundle
  bytes and the expected 256×256 RGB format. Paths and image hashes are unique.
  No selected image is marked excluded.
- Each class/surface contributes 480 training and 120 validation images:
  **2,880 training / 720 validation**. All parent IDs are blank.
- Independently reproduced normalization from the 2,880 training images, using
  the deterministic 224×224 center crop. Mean and standard deviation match the
  saved values to numerical precision; validation images were not used.
- Recomputed overall, per-surface and aggregate metrics for all three seeds from
  the saved 720-image prediction files. Paths, labels, surfaces, parent fields and
  thresholded predictions match the manifest. Histories match selected metrics.
- All 24 methodology bibliography keys exist in the metadata snapshot.

| Seed | Selected epoch | Stopping epoch | Validation macro F1 |
|---|---:|---:|---:|
| 42 | 85 | 100 | 0.764896 |
| 1337 | 78 | 93 | 0.747441 |
| 2026 | 88 | 100 | 0.769095 |

These are validation-selected development results. Mean macro F1 is 0.760478,
with sample standard deviation 0.011483 across optimization seeds on the same
validation images. The three seeds are not three independent datasets.

## Findings that affect the next run

### 1. MobileViT has no standalone Drive workflow or resumable checkpoints

Location: `notebooks/02_mobilevit_baseline.ipynb`, cells 2, 4, 10 and 12.

Dataset discovery uses the absolute `dataset_root` recorded by the local audit.
Outputs use relative local paths. The portable ZIP does not supply that local
summary path, and the audit's recorded computer path will not exist in Colab.
Checkpoints save only inference weights and selected metrics. Optimizer, scaler,
RNG states, phase progress and loader states are absent; history/checkpoint writes
are not atomic. Rerunning resets history and repeats training in the same directory.

Required before launch: a standalone Colab entry point that caches the existing
bundle locally, verifies the frozen manifest and image hashes, and saves atomic
per-epoch recovery checkpoints plus configuration to a separate MobileViT run
folder in Drive. Resuming must retain head/full phase progress and optimizer state.

### 2. The legacy training and reporting recipe is too limited for this comparison

Location: `notebooks/02_mobilevit_baseline.ipynb`, cells 2, 8 and 10;
`notebooks/04_evaluation_and_analysis.ipynb`, cells 2–6.

MobileViT currently uses seed 42, three head epochs and five fine-tuning epochs,
batch 32, head LR 1e-3, fine-tuning LR 1e-4 and weight decay 1e-4. It selects by
binary crack F1 and does not implement early stopping or a learning-rate schedule.
CrackFusion uses seeds 42/1337/2026, effective batch 64, up to 100 epochs, warm-up
and cosine decay, minimum 30 epochs, patience 15 and validation macro F1 selection.

The old evaluation notebook expects a single checkpoint/history and re-runs model
inference. It does not produce the same three-seed, per-surface metric schema as
the completed CrackFusion run. Its curve labels hard-code the old eight-epoch recipe.

Required before launch: freeze a documented MobileViT transfer recipe, run all
three seeds, use the same selection metric and default threshold, and export the
same per-image predictions and metric fields. Reuse the existing verified data,
metric and recovery logic when building the Colab entry point. Different transfer
learning schedules may be justified, but must be predeclared and reported.

### 3. Shared data alone does not make MobileViT a controlled architecture baseline

MobileViT loads ImageNet-pretrained weights, while CrackFusion was initialized from
scratch. The official MobileViT-XS configuration uses 256×256 inputs, bicubic
interpolation, crop fraction 0.9, mean `(0,0,0)` and standard deviation `(1,1,1)`.
CrackFusion uses 224×224, training-derived normalization and its own crop policy.
The legacy MobileViT augmentation also includes different jitter settings and
operation order. Its binary model's exact parameter count still needs measuring
in the actual runtime; the published ImageNet classifier count is not that count.

Use MobileViT as the **practical pretrained reference** specified by the current
experimental protocol, and disclose these differences. Resolve preprocessing from
the actual checkpoint; do not blindly substitute generic ImageNet mean/std or
CrackFusion normalization. Keep both models on the identical frozen validation
tiles. The later causal fusion claim still requires scratch-trained,
parameter-matched CNN-only, Transformer-only and serial-hybrid models.

Sources: [official model card](https://huggingface.co/timm/mobilevit_xs.cvnets_in1k),
[official implementation/configuration](https://github.com/huggingface/pytorch-image-models/blob/main/timm/models/mobilevit.py).

### 4. The trainer ignores the configured threshold when computing metrics

Location: `colab/03_crackfusion_tiny_checkpointed.ipynb`, cells 10 and 12;
the same code is present in local notebook 03.

`evaluate()` and per-surface evaluation call `binary_metrics()` without passing
`THRESHOLD`, so metrics always use its default 0.5. CSV predictions and checkpoints
use the configured value. A reproduced example with probabilities `[0.4, 0.6]`,
labels `[0, 1]` and configured threshold 0.8 returns accuracy 1.0 from the evaluator,
while the configured predictions have accuracy 0.5.

The completed run uses 0.5 and is unaffected. Fix both callers before reusing the
trainer for the new comparison or any secondary threshold study.

### 5. A smoke check can modify pretrained BatchNorm state

Location: `notebooks/02_mobilevit_baseline.ipynb`, cell 6.

The freshly created model is in training mode when the two-image forward check
runs inside `torch.inference_mode()`. Inference mode disables gradient tracking;
it does not set evaluation mode. BatchNorm running statistics can therefore change
before the intended training phases. Run forward checks in evaluation mode and
verify that they preserve the pretrained state.

## Other reproducibility and plan gaps

1. **Resume identity omits training/preprocessing code.** The CrackFusion run ID
   includes the model-source hash and selected settings, but not transform or
   training-helper source. Editing augmentation/scheduling logic can reuse a prior
   run directory and old results. Add those details to new-run provenance and
   enforce compatibility before resuming. Preserve the completed run's identity.
   A seed is reused merely because its metrics JSON exists; also verify required
   predictions/checkpoints before treating it as complete.
2. **Audit recovery is a cache, not fresh verification.** Extraction journals skip
   completed files when their size matches. A diagnostic confirmed that a changed
   same-size file is accepted on rerun. The image-audit journal likewise skips
   previously recorded paths without checking their current content. Training's
   SHA-256 checks protect the selected subset. Before exporting a future modified
   dataset, revalidate cached files or explicitly invalidate the journals.
3. **Research documents diverge.** The current protocol/README use MobileViT as the
   transfer reference and report 284,337 CrackFusion parameters. The methodology
   generator still specifies ResNet-18, a 1–3M target/exit criterion, and a diagram
   with an extra local projection absent from the implemented graph. The literature
   review and methodology assign different meanings to A1–A3 and differ on whether
   gating is required. Consolidate the current experiment matrix and update the
   methodology source/PDF without enlarging the model just to meet an old estimate.
4. **Final-study code remains incomplete.** Verified parent mapping and grouped
   train/validation/test allocation, all three held-out-surface rotations, matched
   baselines, required ablations, parent-cluster paired uncertainty, controlled
   efficiency measurements and branch explanations remain future work. Optional
   timing cells use only 5 warm-up / 20 timed iterations at batch 1, below the
   methodology's research measurement recipe. These gaps do not prevent a clearly
   labelled development comparison; they prevent final architectural claims.
5. **Record versions and metric names explicitly.** Requirements specify minimum
   versions, not a frozen training environment. Record timm, checkpoint revision,
   Python, CUDA and hardware alongside Torch/torchvision in the MobileViT run.
   Standardize `average_precision` across models: the old `pr_auc` field computes
   average precision, not trapezoidal PR area. Do not mix the two definitions.

## Minimal continuation plan

1. Align the current protocol and experiment matrix, retaining the development
   subset stage and later full-data stage as separate recorded phases.
2. Prepare `colab/02_mobilevit_baseline_checkpointed.ipynb` and matching local entry
   point using the existing bundle and the exact CrackFusion manifest hash.
3. Fix the shared threshold callers; use three seeds, atomic Drive recovery,
   complete configuration provenance and a compatible prediction/metric schema.
4. Before long training, verify the actual timm checkpoint download, preprocessing,
   finite single-logit forward output, parameter count, phase transitions and
   checkpoint reload in the intended runtime. GPU training itself remains pending.
5. Report readiness to the user, then start the agreed MobileViT run. Compare
   per-seed and per-surface development results on the identical 720 tiles.

The local Python available to this audit lacks Torch, torchvision, timm and pandas.
The checks executed here use the existing dependency-light recovery checks,
NumPy/scikit-learn/Pillow, recorded run artifacts and isolated evaluator stubs.
The prior Colab evaluation already executed successfully. No claim is made that a
new MobileViT forward/backward or CUDA resume has been verified during this audit.

## Reproduce executed checks

From the repository root:

```bash
python3 scripts/check_drive_checkpoint_recovery.py
python3 outputs/codebase_audit/verify_saved_run.py
```

The second command checks the downloaded completed-run artifacts and all 3,600
local/bundled images, then demonstrates the configured-threshold defect. It is an
audit diagnostic and intentionally reports that currently reproduced defect.


## Resolution after Colab-first consolidation — 6 October 2026

- Four canonical standalone notebooks now replace separate local and Colab copies.
  Shared environment, data validation, atomic writes, metrics, trainer and preflight
  cells propagate from notebook 03 by stable tags. The model lives in that notebook;
  no runtime dependency on the removed src folder remains.
- MobileViT uses the audited bundle, three seeds, validation macro-F1 selection,
  effective batch 64, atomic epoch recovery, optimizer/scaler/RNG state and a saved
  head/full phase. Head training freezes backbone BatchNorm. The official pretrained
  smoke check runs in evaluation mode and verifies unchanged buffers.
- MobileViT's instantiated binary classifier has 1,933,233 parameters with timm 1.0.20.
  The real local preflight verified all 3,600 selected image hashes, finite backward
  execution and checkpoint loading using the official 256-pixel preprocessing.
- Dependencies now include the compatible Hugging Face downloader. Pretrained download
  cache is stored under Drive outputs/pretrained_cache in Colab.
- Overall and surface metrics now use the configured threshold. New run identities
  fingerprint executable training/model/transform code, pretrained backbone weights,
  manifest and software versions. Completed seeds validate their required artifacts
  and predictions before reuse. Historical run_4d1bf234e5ee01bc is preserved.
- Extraction reuse checks ZIP CRC as well as size; audit journal reuse rechecks content
  hashes. Local audit paths work from the root or notebooks directory.
- The unified evaluation reproduced every saved CrackFusion overall, surface and
  aggregate metric. Paired-comparison exports and the retained MobileViT architecture
  inspection also passed with disposable fixtures.
- CPU synthetic interruption tests produced exactly identical final weights and
  histories to uninterrupted runs for both models, including MobileViT's head/full
  transition. These tests do not substitute for a complete CUDA experiment.
- Literature and reference metadata are consolidated under docs/literature; protocol,
  audit and visually checked methodology are under docs/planning. The methodology
  now agrees on the MobileViT reference, 284,337-parameter graph and core ablations.
- All four Drive notebook cell sources were read back and matched their repository
  copies. Existing audit/CrackFusion/evaluation IDs were retained; MobileViT was added.

Colab currently refuses GPU allocation because this account has reached its GPU usage
limit; a CUDA preflight and long training must wait for GPU availability.

No long MobileViT training was started. Verified parent mapping, final source-separated
splits, matched models, full ablation results, held-out surfaces, parent-cluster
uncertainty and publication efficiency measurements remain future study work.

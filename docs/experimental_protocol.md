# Experimental Protocol

## Research question

Under source-separated and cross-surface evaluation, does one explicit fusion of
lightweight convolutional local features and Transformer global features improve
concrete-crack classification over parameter-matched single-family baselines?

## Data

SDNET2018 is the primary dataset. It contains 56,092 image tiles derived from 230
source photographs across deck, wall, and pavement surfaces. Every final split must
keep all tiles from one source photograph in the same partition.

The data-audit notebook inventories files, verifies image readability, hashes exact
duplicates, records surface and class labels, and accepts parent identifiers only
from a documented mapping. When parent identifiers are unavailable, it may create a
fixed tile-level development split for pipeline checks. Results from that split must
remain labelled preliminary.

## Models

The study uses these model families:

- pretrained MobileViT-XS as a practical transfer-learning reference;
- a parameter-matched CNN-only model;
- a parameter-matched Transformer-only model;
- a serial convolution-to-Transformer hybrid;
- CrackFusion-Tiny with parallel local and global branches and one concat-plus-1×1
  convolution fusion point.

CrackFusion-Tiny uses a 224×224 RGB input, a depthwise residual convolutional stem,
a 14×14 grid of 96-dimensional tokens, two four-head Transformer encoders, and one
binary output logit. The implemented graph has 284,337 trainable parameters.

## Training

Matched models are trained from scratch with the same data partitions, augmentation
policy, loss family, optimization budget, and fixed seeds. The primary optimizer is
AdamW with weighted binary cross-entropy. The positive-class weight is computed from
the training partition only; it is not combined with balanced sampling in the main
experiment.

Validation data control checkpoint selection, early stopping, and any secondary
decision threshold. The final test partition remains sealed until model and
hyperparameter choices are fixed.

## Evaluation

Primary outcomes are crack recall, F1, average precision, and balanced accuracy.
Precision, specificity, ROC-AUC, confusion matrices, parameter count, latency, and
peak memory are also reported. Principal comparisons use three fixed seeds and
include per-surface results.

Cross-surface evaluation uses three rotations:

- train on wall and pavement; test on deck;
- train on deck and pavement; test on wall;
- train on deck and wall; test on pavement.

No hyperparameter or threshold may be selected using the held-out surface.

## Current evidence boundary

The repository currently contains software-validation checks and a preliminary
MobileViT development workflow. It does not yet contain source-separated CrackFusion
results or evidence of field-ready structural diagnosis, crack-width estimation,
segmentation performance, universal generalization, or state-of-the-art accuracy.

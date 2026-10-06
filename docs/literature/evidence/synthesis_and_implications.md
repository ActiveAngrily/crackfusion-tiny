# Cross-domain synthesis and implications for the paper

**As of:** 6 October 2026. This synthesis combines the first-pass and follow-up workstreams catalogued in the [review index](survey_index.md). It describes what the reviewed evidence supports and how it bears on the current protocol; it does not report experimental results for CrackFusion-Tiny.

## 1. The domain has several distinct prediction tasks

“Crack detection” is used as an umbrella term across unlike problems:

| Task | Output | Evidence needed |
|---|---|---|
| Image/patch classification | One label or score per crop (for example, crack / no crack) | Group-aware classification metrics and a clear image/source split. |
| Object detection | Bounding boxes or candidate crack regions | Box annotations and detection metrics such as AP/mAP. |
| Semantic or instance segmentation | Pixel masks or separated objects | Dense annotations and mask/boundary metrics such as IoU, Dice and pixel recall. |
| Crack measurement or structural diagnosis | Physical dimensions, severity, or engineering risk | Calibrated geometry/material context, defensible labels and validation against suitable measurements or decisions. |

The present paper is about binary image classification. Results from segmentation, object detection, severity classification, 3D scans, or crack-width measurement can motivate methods, but cannot act as direct classifier baselines or establish those capabilities for this model. See [03](crack_detection_segmentation.md) and [06](reviews_and_research_position.md).

## 2. Architecture evidence supports a hypothesis, not a guaranteed gain

Convolutions supply useful local and translation-biased processing; Transformers and other attention mechanisms offer context aggregation. General-vision work has already explored serial stages, interleaved blocks, concurrent streams, latent-token exchanges, and repeated or late fusion. MobileViT, Conformer, Mobile-Former, CvT, CMT and later mobile hybrids make local/context interaction established architecture territory. Crack-specific classification and segmentation papers also combine convolution and attention.

CrackFusion-Tiny is a particular compact layout: a shared convolutional stem, parallel local depthwise-CNN and 196-token Transformer paths, one concatenation plus 1×1 projection, global pooling and one binary logit. The code has 284,337 trainable parameters. This is a describable design choice, not evidence that fusion helps. EfficientCrackFusion is a March 2026 preprint that directly establishes parallel local/global branches and adaptive cross-attention fusion for binary crack classification; the project cannot claim to be first in those broad categories. Its stated ViT-Base backbone conflicts with its reported 12.8M total parameters, so its efficiency figures are not reliable without clarification. Sait et al. (2026) provide another staged/parallel local-global precedent. CrackNeXt and DBD-KD remain date/full-text unresolved; DBD-KD's accessible snippets do not establish that both distillation branches remain in the student inference graph. Resolve chronology and inspect primary texts before time-bounded novelty wording.

The defensible contribution, if experiments are completed, is an evidence-quality contribution: a clearly specified small classifier assessed on source-photo-separated data, with controlled architecture comparisons and cross-surface results. It must not be framed as inventing CNN–Transformer crack classification or feature fusion. See [01](crack_classification.md), [02](hybrid_architectures.md), and [06](reviews_and_research_position.md).

## 3. Data lineage is the central validity gate

SDNET2018 contains 56,092 256×256 tiles from 230 original photographs, with 8,484 crack tiles and 47,608 non-crack tiles. Its apparent sample size is not its independent acquisition count. Tiles from one photograph share surface texture, lighting, camera response, and potentially nearby crack patterns. A random tile split can therefore measure interpolation among related crops rather than generalization to a new source photograph. This is a risk to test, not proof that any particular published score is inflated.

The current audit leaves parent IDs blank unless a documented tile-to-source mapping is available. The official USU metadata was readable, but the archive file endpoint returned 403, so the downloadable readme/zip contents were not inspected; the survey does not conclude that the release lacks originals or a map. No complete, verified tile-to-parent mapping has been established. The 3,600-image development subset is labeled `tile_development_only`. Consequently, **the project does not yet have evidence for source-photo-held-out performance**. Exact duplicate hashing cannot recover sibling crops or prove common origin; inferred image similarity is not a provenance map.

The survey found a useful protocol contrast: Zhang et al. (2026) report keeping tiles from each source photo in one partition on a balanced 16,800-tile subset; AttXNet v2 uses stratified tile-level splitting and explicitly acknowledges correlation risk. This shows both that source grouping is feasible in some dataset derivatives and that a high headline score on random tiles does not answer the grouped question. See [04](datasets_generalization.md).

## 4. Domain shift is established, but it is multidimensional

Prior cross-domain studies report that within-collection performance can fall sharply on new collections. One CCIC-to-Itaipu classifier study reports above 99% source accuracy and about 54% on 118 target patches from only three photographs; this is a strong warning to test transfer, but too few independent target sources to estimate field-wide performance. A 2025 multi-dataset study also reports large cross-test drops but uses random image-level partitions and single runs. Mixed acquisition, labels and class balance prevent treating these exact scores as a universal shift estimate.

The planned leave-one-surface-out evaluation (deck, wall, pavement) is a useful composite transfer test. A held-out surface changes more than material surface alone: structure type, setting, crack prevalence, illumination, camera/viewpoint and acquisition conditions may co-vary. With three target categories, the result supports statements about those held-out SDNET surfaces, not a causal “surface effect” or universal field generalization. An external dataset is stronger only when its source lineage, duplicate overlap, labels, acquisition unit and class semantics are audited. Composite datasets can silently include SDNET or derivatives.

## 5. Metrics, thresholds and uncertainty must match the sampling process

SDNET’s crack prevalence is about 15.1%; predicting every tile as non-crack yields about 84.9% accuracy and zero crack recall. Keep natural prevalence for final testing. Report crack-positive recall, precision, F1, average precision/PR curve, balanced accuracy, specificity and confusion matrices, with positive-class and threshold definitions. AP is prevalence-sensitive and should not be relabeled as trapezoidal PR-AUC without matching the implementation. Calibration is needed if scores are described as probabilities or risk.

Choose checkpoints, hyperparameters and any non-default threshold using training/validation data only. In LOSO, never select a threshold or model using the held-out surface. Report all seed runs. Three seeds describe optimization variation conditional on the same split; they are not independent datasets. Where source-photo testing is possible, paired uncertainty comparisons should resample parent photos with all their tiles. If the intended population is new structures or campaigns, photos may still be nested within a smaller number of higher-level clusters. State whether each score is tile-weighted or photo-weighted and what population it estimates.

The CCTNet SDNET table provides a concrete reporting caution: five printed fold accuracies average to 98.90%, but the paper labels their average 98.04%. A newly surfaced 2026 SDNET threshold study supplies another operating-point lead, but only its abstract was accessible and split grouping is unresolved. Internal arithmetic mismatches, unclear group splits, and nonstandard metric naming make method and table-level auditing more useful than comparing headline numbers. See [01](crack_classification.md), [04](datasets_generalization.md), and [09](search_completeness.md).

## 6. Fair model comparisons require matching training as well as architecture

Pretrained MobileViT-XS is a practical transfer-learning reference. It is not a clean causal comparison with CrackFusion-Tiny or scratch-trained parameter-matched controls: initialization, pretraining data, augmentation and recipe differ. To attribute a gain to fusion, compare the local-only, Transformer-only, serial CNN→Transformer, and fused configurations on identical grouped partitions with the same preprocessing, augmentation policy, optimizer family, training/selection budget and seeds. Match capacity as closely as practical, document remaining differences, and preserve a separate pretrained reference. A branch ablation is more informative than adding speculative attention machinery.

## 7. Compactness does not establish deployment speed

The 0.284M parameter count supports a model-size description only. It does not establish checkpoint size, FLOPs/MACs, memory use, latency, energy or edge readiness. Efficiency evidence in the literature varies by resolution, task head, device, runtime, precision, batch size, warm-up and whether preprocessing is timed. AttXNet’s 825 FPS is ground-station-assisted batch patch throughput, not onboard UAV or batch-1 phone latency. Segmentation FPS is not comparable with classifier FPS. See [05](efficiency_and_deployment.md).

For a defensible comparison, report the instantiated graph and checkpoint, input/preprocessing, operation counter and convention, named device/runtime, precision, batch-1 latency and batched throughput separately, warm-up/repetitions, timing boundaries, memory, and energy only when directly measured. A 2026 UAV/TinyML classifier is a direct task precedent; its abstract-level report includes F1 0.938, 2.9 MB RAM, 309 KB flash, 461.6 ms latency, and 623.16 mJ per inference. Verify its full methods, device/runtime, split, and energy boundary before using those values as a comparison. Temporal video, point-cloud, thermal, and RGB-D papers address system-level or different prediction tasks; see [14](deployment_multimodal_and_temporal.md). Keep quality and efficiency paired on the same frozen test examples.

## 8. Interpretability maps are diagnostics, not proof

Grad-CAM can show which convolutional feature regions influence a target logit; attention rollout/flow approximates token relevance. Both can help inspect true/false positives and spurious cues such as shadows, joints and stains. Neither proves causal use of cracks, pixel-level localization accuracy, physical measurement, or structural understanding. Without mask labels, visual overlap is qualitative. A faithfulness claim needs model/label-randomization checks and a predeclared perturbation test with controls; localization needs annotated masks, while physical width and severity need calibrated reference measurements and operational labels. See [13](interpretability_measurement_and_task_extensions.md).

## 9. Claim boundary for the manuscript

| Claim | Current support |
|---|---|
| Crack classification literature spans CNN, Transformer, serial, parallel and mobile hybrids. | Supported by the screened primary-source corpus. Avoid “first hybrid” claims. |
| A compact explicit local/global classifier is implemented. | Supported by source code: 224×224 input and 284,337 trainable parameters. |
| The proposed model improves source-separated performance or fusion helps. | Not established; requires verified parent mapping and matched experiments. |
| The model generalizes across concrete surfaces or external sites. | Not established; requires locked LOSO/external tests with audited provenance. |
| The model is faster, deployable, real-time, or energy-efficient. | Not established; requires controlled platform measurements. |
| The model localizes, measures, grades or diagnoses structural cracks. | Outside the image-label task and unsupported by current outputs. |

## 10. Research sequence implied by the survey

1. **Recover and document the SDNET tile-to-parent-photo mapping.** If that cannot be verified, retain results as development-only and revise the paper's research question accordingly.
2. **Lock source-photo partitions and manifests before training.** Audit duplicate overlap and publish group counts by surface and class.
3. **Run the matched architecture ablations and the separate pretrained reference.** Freeze thresholds and model selection on validation only.
4. **Report per-surface metrics, seed spread and parent-cluster uncertainty.** Describe LOSO as composite domain shift.
5. **Measure efficiency on a named target platform** only if compact deployment is part of the paper's claim.
6. **Refresh date-sensitive literature and resolve CrackNeXt's and DBD-KD's online-first dates and primary-text details** before final novelty language; close the abstract-only classifier candidates and run reproducible database exports before submission.

Robustness to controlled blur, noise, exposure, compression and occlusion, group-count learning curves, and in-domain self-supervision are defensible follow-on experiments, but they are secondary to source mapping and a valid held-out protocol. Add video, 3D, thermal or RGB-D inputs only if the paper changes from still-image binary classification to an explicit multimodal or inspection-system question.

The first item is a go/no-go gate for source-separated performance claims. The remaining items follow from whichever contribution the completed data and experiments can substantiate.

# Efficiency and deployment evidence

**Scope.** Targeted survey of efficiency and deployment reporting for binary crack-image classification. Closest segmentation deployment papers appear only as adjacent context. Segmentation FPS is not comparable with classifier FPS because dense mask prediction, input dimensions, decoders and post-processing change the workload. This note is not an exhaustive systematic review.

## Project-specific baseline

The implemented CrackFusion-Tiny takes 224×224 RGB and has 284,337 trainable parameters ([model source](../../../notebooks/03_crackfusion_train.ipynb)). This is a measured graph parameter count, not an inference-speed or deployment claim. The MobileViT-XS reference is pretrained and its 1000-way head is replaced; its exact binary-model count, transform, and checkpoint bytes must be measured in the target run. Original MobileViT-XS figures (~2.3M parameters, 256×256) describe the ImageNet model, not the task-modified checkpoint. The codebase audit says current optional timing (5 warm-ups, 20 batch-1 iterations) is insufficient for research reporting and no controlled efficiency measurements exist yet ([audit](../../../outputs/codebase_audit/2026-10-06.md)).

## Evidence table

| Work / task | Workload and reported evidence | Relevance and limits |
|---|---|---|
| Mehta & Rastegari, MobileViT (ICLR 2022), general classification | MobileViT-XS: ~2.3M parameters, 74.8% ImageNet-1K top-1, 256×256 input in the original model. Paper includes mobile latency and memory comparisons. [Paper](https://openreview.net/forum?id=vh-0sUt8HlG) · [Apple implementation](https://github.com/apple/ml-cvnets) | Primary architecture reference. Device timing is implementation/device-specific and cannot stand in for our `timm` one-logit model. Paper also illustrates why FLOPs alone do not determine latency. |
| Şermet & Pacal (2024), SDNET2018 crack classification | MobileViT XS/S/XXS and CNN/ViT comparison; 224×224 preprocessing, ImageNet transfer learning, 70/15/15 image split. [Article](https://dergipark.org.tr/en/pub/dumf/article/1450640) · [full text](https://dergipark.org.tr/en/download/article-file/3785322) | Closest MobileViT task precedent. The paper does not establish that tiles from a parent photo stay in one partition; scores are not directly comparable with source-photo-separated evaluation. No reproducible device/energy protocol was established from accessible sections. |
| Gao et al. (2023), smartphone bridge crack detection | SSD + sliding-window scanning and neighborhood correction deployed through Android/TensorFlow. Huawei Honor 7i, octa-core 1.5 GHz, 3 GB RAM, Android 6.0.1. [Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC10450596/) | Practical portable-device precedent. Retrieved system table identifies platform, but no standardized per-image latency, throughput, energy or model size was found. Detector/sliding-window processing is not one-pass 224px classification. |
| Chunkaew et al. (2026), mobile-oriented concrete severity classification | MobileNet/VGG-16/ResNet-50; 1,634 images, 10 categories, 224×224 RGB. MobileNet reports 80% accuracy and 13.1 MB model size. [DOI/article](https://doi.org/10.11591/ijai.v15.i3.pp2811-2825) | Size and task context are useful; accessible abstract does not give device/runtime, precision, batch, latency or energy. Different task/dataset. |
| Zhang et al. (2026), TinyML UAV crack classification, Scientific Reports | Abstract reports F1 0.938, RAM 2.9 MB, flash 309 KB, end-to-end latency 461.6 ms, energy 623.16 mJ/inference; DJI Mini 4 Pro flight-time reduction 1.31 min (4%) versus 8 min (24%) for Jetson platform. [DOI/full article](https://doi.org/10.1038/s41598-026-43534-4) · [publisher text](https://www.nature.com/articles/s41598-026-43534-4) | Excellent example of RAM, flash, latency, energy and system-level cost reporting. Keep end-to-end boundary explicit; extract exact sensor/model/input/backend details from article before making specific implementation comparisons. |
| Chen et al. (2026), MCANet-Tiny, pavement crack classification | MobileNetV3-Small with coordinate attention and pruning. Abstract reports 0.12M parameters, 0.02 GFLOPs, 92.1% fewer parameters, 83.3% fewer FLOPs; INT8 Huawei P50 Pro: 166.67 FPS at 94.26%; platforms include Radxa Cubie A7A and Orange Pi 3B. [DOI/article](https://doi.org/10.1016/j.eswa.2026.132915) | Peer-reviewed recent classifier evidence. Abstract lacks input resolution, batch, timing boundaries and runtime/compiler; full text access was denied. Do not use headline FPS as directly comparable until protocol verified. Asphalt domain differs. |
| Wang et al. (2026), DBD-KD, crack classification | Dual-branch frequency/spatial knowledge-distillation framework; abstract reports no added inference cost and 97.1% on Road Distress Dataset, 93.2% on SDNET2018(W), 87.4% on CQU-BPDD. [Publisher](https://www.sciencedirect.com/science/article/pii/S0167865526003363) | No device, latency, memory, or energy protocol was visible in accessible publisher text. Publisher describes random 70/15/15 image-level splits. Full text unavailable; volume date Nov 2026, while a [secondary 19 September listing](https://www.ebiotrade.com/newsf/2026-9/20260919001010972.htm) suggests possible earlier online publication. Official online-first date remains unresolved. Treat as candidate prior art, not verified efficiency evidence. |
| Li et al. (2026), AttXNet / “Robust Lightweight Crack Classification for Real-Time UAV Bridge Inspection” (arXiv v2) | Full HTML v2 describes 825 FPS as **ground-station-assisted batch patch throughput** on SDNET2018 bridge-deck data; reports 11.21M parameters and 1.82G FLOPs. [arXiv v2 HTML](https://arxiv.org/html/2604.27617v2) · [code](https://github.com/skylynf/AttXNet) | This is not an onboard UAV measurement or batch-1 mobile latency. The evaluation uses a tile-level split and does not establish parent-photo grouping, so leakage/generalization risk limits the reported score. Treat 825 FPS as a specific ground-station batch throughput claim, not portable edge latency. Preprint. |
| Huang et al. (2024), CrackScopeNet, crack segmentation | Lightweight segmentation designed for resource-constrained drone/mobile platforms; reports outdoor mobile-device deployment. [Article](https://doi.org/10.3390/drones8090417) | Adjacent segmentation evidence only. Dense predictions, resolution and post-processing prevent direct FPS comparison with classification. |
| EfficientCrackNet (2024 preprint), segmentation | Depthwise separable convolutions plus MobileViT block; Crack500, DeepCrack, GAPs384; abstract reports 0.26M parameters and 0.483 GFLOPs. [arXiv](https://arxiv.org/abs/2409.18099) | Similar parameter count does not imply similar classifier runtime; segmentation workload. |
| EfficientSegNet (2025), drone-image crack segmentation | Lightweight multi-scale segmentation; abstract reports mIoU increase from 55.55% to 80.81% “while maintaining inference speed.” [DOI/article](https://doi.org/10.1016/j.conbuildmat.2025.143667) | Adjacent context only; accessible abstract lacks enough platform/timing detail for cross-paper speed comparison. |

### FLOPs and model-size accounting

MobileViT-XS FLOP totals vary across implementations and counting conventions. The original ICLR 2022 work/model references use ~2.3M parameters and a 256px input; an ICLR 2025 comparison table lists 0.986G FLOPs at 256, while other mobile comparisons report around 0.9G. These values are not crack-task measurements. [ICLR 2022](https://openreview.net/forum?id=vh-0sUt8HlG) · [ICLR 2025 TinyML vision paper](https://openaccess.thecvf.com/content/ICCV2025/papers/Zeng_An_Efficient_Hybrid_Vision_Transformer_for_TinyML_Applications_ICCV_2025_paper.pdf)

FLOPs/MACs depend on tool and convention (one multiply-accumulate may be counted as one or two operations). Parameter count is not checkpoint size, and neither metric predicts latency by itself. Report the operation counter/version, input shape and convention. For MobileViT, count the instantiated binary task graph rather than quoting the original 1000-class head. Separate theoretical cost, batch throughput, single-image latency, and full pipeline latency.

## Synthesis for the paper

1. CrackFusion-Tiny’s small parameter count supports a compactness statement only; it does not establish speed, energy efficiency or deployment readiness.
2. Report two distinct comparisons: controlled efficiency at identical 224×224 input/settings, and MobileViT-XS as the practical pretrained reference with its checkpoint-specific preprocessing and any 256px input. Disclose input differences rather than presenting them as an architecture-only comparison.
3. Do not pool platform-specific FPS figures. Missing batch, precision, runtime, input size or timing boundary makes a headline rate non-comparable.
4. Keep segmentation speed in adjacent-work prose only, never in the classifier leaderboard.

## Reporting checklist

For every classifier, record:

- exact graph/head, total and trainable parameters, pretrained source/revision, initialization policy and task checkpoint bytes;
- input size and preprocessing; whether preprocessing/postprocessing is timed;
- MACs/FLOPs, counter/version and operation convention;
- device/model and CPU/GPU/NPU, OS, framework/runtime/backend/delegate, compiler, threads and power mode;
- FP32/FP16/INT8 precision, calibration, batch size, warm-up/repetitions, synchronization, and latency summary (median and p95 or spread);
- batch-1 latency separately from batched throughput; model load/start-up separate; preprocessing, forward and end-to-end timings;
- peak RAM/accelerator memory, deployed artifact/flash bytes, and measured energy only with instrument/method and run conditions;
- quality metrics including crack recall/F1/AP on the same frozen test examples; source-photo grouping and cross-surface status; distinguish seeds on one split from independent domains.

**Proposed minimum for this project (not yet executed):** on one named device, compare CrackFusion-Tiny and binary MobileViT-XS at batch 1, eval mode and FP32. Warm up 50 runs; time at least 500 synchronized runs; report median and p95; separate preprocessing, forward and end-to-end. Record checkpoint bytes, parameter count and operations at the stated input size. If MobileViT stays at its official 256px transform, publish it as a practical-baseline measurement and retain a separate matched-resolution comparison for controlled efficiency.

## Search, reading and access log

Search date: 6 October 2026. Targeted queries covered “MobileViT XS parameters FLOPs latency”, crack classification/mobile/edge/TinyML/UAV deployment, SDNET2018 device benchmarks, smartphone bridge crack systems, quantization, energy and recent 2024–2026 reports. Sources were screened by task (classification first; detection/segmentation only as context).

| Source | Reading/access status | Notes |
|---|---|---|
| Repository README, experimental protocol, model source, old MobileViT comparison and `outputs/codebase_audit/2026-10-06.md` | Read in full | Established model shape/count, baseline status, current measurement gap. |
| MobileViT ICLR 2022 | Primary paper page and search-indexed PDF metadata/tables consulted; direct PDF opening blocked by OpenReview verification. Official Apple code and later primary comparison tables cross-checked. | Do not claim fresh complete full-text reading; verify exact table-specific latency details before manuscript use. |
| Şermet & Pacal 2024 SDNET/MobileViT | Full downloadable article opened and task/setup read. | Image-level split; source-photo grouping not established. |
| Gao et al. 2023 smartphone bridge study | PMC article text/search extract reviewed, including system table; direct browser open encountered bot check. | Platform recorded; quantitative timing not found in accessible extracted content. |
| Zhang et al. 2026 TinyML UAV classifier | Publisher/PMC metadata and full-text access route reviewed; abstract metrics captured. | Peer-reviewed Scientific Reports; inspect complete methods for exact device/pipeline details before deeper comparative claims. |
| Chen et al. 2026 MCANet-Tiny | Publisher abstract/preview reviewed; full text returned 403. | Platform names and abstract FPS available; timing details unverified. |
| Li et al. 2026 AttXNet | **Full arXiv HTML v2 read.** | Corrected interpretation: 825 FPS is ground-station-assisted batch patch throughput; not onboard/batch-1 mobile. Tile-level split; parent-photo grouping not established. |
| Wang et al. 2026 DBD-KD | Publisher abstract and indexed method/dataset excerpts reviewed; full text unavailable. | No comparable hardware metrics exposed. Image-level splits; publisher issue/online-first cutoff status unresolved. |
| CrackScopeNet 2024 | Abstract/search-indexed article content reviewed; publisher page rate-limited. | Segmentation-only context. |
| EfficientCrackNet 2024 | arXiv abstract reviewed. | Segmentation-only; 0.26M parameters/0.483G FLOPs reported in abstract. |
| EfficientSegNet 2025 | Publisher abstract reviewed. | Segmentation-only; platform protocol unavailable in accessed excerpt. |
| Chunkaew et al. 2026 mobile severity study | Journal abstract and DOI record reviewed. | 224 input, 80% accuracy, 13.1 MB reported; no abstract-level runtime protocol. |

**Coverage limit.** This was a targeted search, not a registered database-by-database systematic review. Several publisher pages limited full-text access. Reported “real-time” and FPS claims are therefore qualified by available measurement details.

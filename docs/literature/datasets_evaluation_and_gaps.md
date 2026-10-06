# Datasets, evaluation, and research gaps

**Tags:** `SDNET2018` `dataset` `parent-photo-split` `data-leakage` `class-imbalance` `cross-surface` `domain-generalization` `metrics` `latency` `severity-datasets` `2025` `2026`

**Last reviewed:** 2026-10-06\
**Scope:** image-level crack/no-crack classification, with related detection, segmentation, and severity datasets included only where they inform data design or future evaluation.\
**Purpose:** connect dataset and evaluation practice in the literature to the current CrackFusion-Tiny experiment.

## Main takeaways

1. SDNET2018 is large in tile count but much smaller in parent-photograph count: its 56,092 tiles were cut from 230 larger concrete photographs. The 230 photos are not necessarily 230 independent structures. A random tile split can put near-neighbor patches from one photo in train and test, so grouping by the documented parent photograph is the sound split unit.
2. Crack/no-crack labels are imbalanced: 8,484 cracked tiles and 47,608 uncracked tiles. An always-uncracked predictor would score about **84.9% accuracy**, so accuracy cannot be the headline metric by itself.
3. A model can score well on an in-dataset test and still transfer poorly to another source, surface, camera, or acquisition setup. Source-separated testing and leave-one-surface-out experiments answer complementary questions.
4. Recent data releases broaden the task, but most are not drop-in external test sets for our binary SDNET2018 experiment. Their labels, materials, scale, and image-acquisition process must match before pooling scores.
5. The project protocol already specifies the right central checks—parent-photo grouping, class-aware metrics, three cross-surface rotations, fixed seeds, and efficiency reporting. The main unresolved dependency is whether we can establish a trustworthy parent-photo ID for every SDNET tile.

## SDNET2018: tiles, source photographs, and label balance

The SDNET2018 data paper describes 56,092 RGB tiles at 256 × 256 pixels across bridge decks, walls, and pavements. It reports 8,484 crack tiles and 47,608 non-crack tiles. Its images include confounders such as shadows, roughness, scaling, edges, holes, and debris. The dataset paper says the images were divided into sub-images from larger photographs; a later peer-reviewed study reports the commonly cited acquisition count as **230 parent images** (72 wall, 54 deck, 104 pavement). ([SDNET2018 data paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC6247444/); [Bhattacharya et al., 2021](https://doi.org/10.1109/TCSVT.2020.3028008))

The tile counts imply a crack prevalence of 8,484 / 56,092 = **15.1%**. Predicting “no crack” for every tile yields 47,608 / 56,092 = **84.9% accuracy**, while detecting no cracks at all. These are calculations from the published counts. The prevalence also varies by surface: deck 14.9%, wall 21.2%, pavement 10.7%. ([SDNET2018 data paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC6247444/))

### Why a tile-level random split is risky

Tiles cut from the same parent photograph may share concrete texture, illumination, camera response, crack geometry, and nearby spatial content. If tiles from one parent are divided across train and test, the test set is less independent than its tile count suggests. This is a risk of overly optimistic measurement, not proof that every previous random split is invalid.

A 2026 crack-classification deployment study explicitly split SDNET2018 at the **original high-resolution photograph** level to reduce spatial correlation between train and test. This is direct precedent for the project’s source-separated design. ([Zhang et al., 2026, *TinyML pipeline for efficient crack classification in UAV-based structural health inspections*](https://doi.org/10.1038/s41598-026-43534-4))

**Practical implication:** all tiles from one parent image should remain in exactly one partition. Keep parent IDs in the audit manifest and record the mapping source. Exact-duplicate hashes can find duplicate files, but they do not establish that two different tiles came from the same photograph. Similarity search can flag candidates for manual review; it should not silently become the provenance mapping.

If the available SDNET archive does not preserve a verifiable parent mapping, a random tile split must remain a pipeline-development result, as the project README and protocol already state. To claim source-independent testing, recover the grouping from documented acquisition data or obtain a separate source-photo test set. Do not infer parent identity from filenames unless the archive documentation supports that interpretation.

## Split design: three different generalization questions

| Evaluation | What stays separate | What it tells us | Main caveat |
|---|---|---|---|
| **Source-separated in-dataset test** | All tiles from each original photograph | Whether performance carries to unseen source photographs drawn from SDNET2018’s acquisition conditions | Still tests the same dataset and acquisition setting |
| **Leave-one-surface-out** | One entire surface type is absent from training and validation, then used for test | Whether features transfer among SDNET2018 decks, walls, and pavements | Surface, class prevalence, and capture context shift together; it does not isolate which factor caused a drop |
| **External dataset test** | Entire dataset/source collection is held out | Whether performance transfers to another collection, camera, material, or labeling pipeline | Comparability depends on matching the task, preprocessing, label definition, and decision threshold |

The current protocol’s three rotations—train on two of deck/wall/pavement and test on the third—are a useful cross-surface test. The held-out surface must not influence hyperparameters, checkpoint choice, or threshold. Within the training surfaces, source photographs still need to be grouped when making train/validation splits. Report every rotation separately, since averaging can hide a surface-specific failure.

Recent research supports the need for transfer tests. A 2025 study evaluated CNN, ResNet50, LSTM, and VGG16 across six public structural-surface crack datasets. It found substantial performance loss in cross-testing compared with each dataset’s self-test, with results affected by image resolution, texture, and environmental noise. Its study is a useful generalization reference, not a direct score comparison with CrackFusion-Tiny because its datasets, splits, and models differ. ([Rashid et al., 2025](https://doi.org/10.1515/jmbm-2025-0074))

## Metrics for binary crack classification

SDNET2018’s imbalance makes it important to show the positive-class behavior explicitly.

| Metric | Why report it |
|---|---|
| Crack recall | Directly shows how many crack tiles are missed or found; a high miss rate can be hidden by accuracy. |
| Crack precision | Shows how often a crack alert is correct, which matters when false alarms create inspection work. |
| Crack F1 | Summarizes the precision–recall trade-off at the selected operating threshold. State which class is positive. |
| Average precision / precision–recall curve | Summarizes ranking quality with crack as the positive class; report test prevalence because AP depends on prevalence. |
| Balanced accuracy | Averages crack and non-crack recall, giving both classes equal weight. |
| Specificity, ROC-AUC, confusion matrix | Useful complementary views; ROC-AUC is threshold-independent but does not replace crack precision/recall under imbalance. |

Keep the test set at its natural class distribution. Do not balance or downsample the final test set merely to make accuracy look fairer: that changes the evaluation prevalence and the practical precision context. Training can use a training-only class weight, as this project specifies. Choose checkpoints and any optional threshold using validation data only; the test threshold must not be tuned after looking at test outcomes.

For the three-seed plan, report each seed and a mean with spread rather than only the best run. If uncertainty intervals are added, resample parent photographs (groups), not individual tiles, so the interval does not treat correlated tiles as independent observations. Since SDNET2018 has relatively few parent photographs and only three surface categories, describe those intervals carefully and do not overstate them as broad population guarantees.

## External and recent datasets: what is useful, and what is not interchangeable

| Dataset or resource | What it contributes | Fit to this paper |
|---|---|---|
| **SDNET2018** ([data paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC6247444/); [official Utah State record](https://digitalcommons.usu.edu/all_datasets/48/)) | Main binary concrete dataset; decks, walls, pavements; 56,092 tiles from parent photographs | Primary dataset. Needs verifiable parent-photo groups for final source-independent results. |
| **Concrete Crack Images for Classification (CCIC)** ([Mendeley Data record](https://data.mendeley.com/datasets/5y9wdsg2zt/1)) | 40,000 balanced 227 × 227 concrete patches (20,000 per class), extracted from 458 high-resolution source photographs collected on METU campus | Potential external check after verifying label policy and input preparation. If used for training or internal validation, group by its 458 source photographs. Its different campus, source photographs, and balance make it a useful domain-shift test, but reported scores should retain its own prevalence/context. |
| **2025 cross-dataset classification study** ([paper](https://doi.org/10.1515/jmbm-2025-0074)) | Reports SDNET2018 plus five other collections (SCD, CPC, CDIBM, CCI, HBC) and tests source-to-target transfer | Useful protocol precedent. Dataset acronyms and exact label mapping should be checked from the paper before selecting any as an external benchmark. |
| **Attain pavement-distress dataset (2025)** ([data article](https://doi.org/10.1016/j.dib.2025.111715)) | 2,293 road images, 19,761 annotated distress instances, ten distress categories, expert annotations, and severity levels; collected with smartphone cameras | Useful for future object-level pavement distress/severity studies. It is not a direct external test for concrete crack/no-crack tiles: scene framing, material, classes, instance labels, and severity task differ. |
| **Multi-temporal Crack Segmentation Dataset (2025)** ([Zenodo record](https://doi.org/10.5281/zenodo.15187675); [ISPRS paper](https://isprs-annals.copernicus.org/articles/X-G-2025/341/2025/)) | 25 high-resolution concrete source images expanded into temporal and mono-temporal patches; includes masks and repeated crack-progression frames | Not a binary-classification dataset. It is a useful warning that many patches or temporal views can come from a small number of physical/source examples; split by original image/structure/sequence for any future use. |
| **HU Infrastructure Cracks v2 (2026)** ([Zenodo record](https://doi.org/10.5281/zenodo.21010220)) | 87 crack records, 900+ high-resolution images, severity labels (11 minor, 52 moderate, 24 severe), pavement and wall records | Promising small external/future-severity resource. Group all views from the same crack record together. Small and severity-imbalanced; version 2 should be pinned explicitly in any study. |
| **PaveTrack (2025)** ([Scientific Data paper](https://doi.org/10.1038/s41597-025-05748-5)) | Large-scale road-distress repository with long-term tracking and multiple distress types | Relevant to temporal pavement maintenance and road-domain transfer, but not a direct match for concrete image-level binary classification. |

The dataset examples above are selected for methodological relevance, not a complete catalog. Dataset names can conceal major differences in what one sample means: a crop, a source photograph, a crack instance, a temporal frame, or a pixel mask. That unit should be recorded before datasets or scores are compared.

## Reporting a “lightweight” model fairly

Parameter count alone does not demonstrate deployability. Report at least:

- trainable parameters and model-file size;
- MACs or FLOPs, with the counting convention and input size;
- inference latency at the same input size, device, runtime, precision, and batch size for every model;
- peak inference memory, and throughput if useful;
- preprocessing and end-to-end latency separately if preprocessing is part of the intended use.

For a mobile or edge claim, measure on the target device or label desktop results as desktop measurements. Include warm-up and repeated timing details. A 2026 TinyML crack-classification paper illustrates fuller deployment reporting by measuring RAM, flash, latency, energy, and UAV flight-time impact, rather than using accuracy or model size alone. ([Zhang et al., 2026](https://doi.org/10.1038/s41598-026-43534-4))

In this project, the pretrained MobileViT-XS is a practical transfer-learning reference; the scratch-trained CNN, Transformer, serial hybrid, and CrackFusion-Tiny are controlled architecture comparisons. Keep those interpretations distinct: the MobileViT reference is not a parameter-matched, same-initialization ablation. The protocol already requires shared splits, training budget, augmentation, loss family, and seeds for the scratch-trained comparisons. ([Project experimental protocol](../planning/experimental_protocol.md))

## What prior reviews and benchmarks cover

- [Hsieh and Tsai, *Machine Learning for Crack Detection: Review and Model Performance Comparison* (ASCE, 2020)](https://ascelibrary.com/doi/10.1061/%28ASCE%29CP.1943-5487.0000918) is a useful foundational review and comparison paper on crack-detection methods.
- [Li et al., *A Review of Deep Learning Methods for Pixel-Level Crack Detection* (2022)](https://www.sciencedirect.com/science/article/pii/S2095756422001027) systematically organizes segmentation architectures, public datasets, metrics, and loss functions. Its main scope is pixel-level detection, so use it for segmentation background rather than as a direct image-classification benchmark.
- [Zhang et al., *Deep Learning for Crack Detection: A Review of Learning Paradigms, Generalizability, and Datasets* (2025 preprint)](https://arxiv.org/abs/2508.10256) focuses on generalization and dataset diversification, introduces 3DCrack, and benchmarks segmentation models. The arXiv record labels it under review; treat it as a preprint, not an established peer-reviewed standard.
- The 2025 cross-dataset classification study above is closer to this paper’s image-level task and supplies direct evidence that single-dataset self-tests do not establish cross-source generalization.

These reviews differ in task scope and inclusion criteria. None supplies a universally accepted split for our exact experiment; the project must state and justify its own data grouping and protocol.

## Implications for the current paper

The binary task remains defensible if the claims are proportionate to the evidence. A credible paper can ask whether one explicit local/global fusion helps a compact classifier **under source-separated and cross-surface evaluation**. The stronger research point is the controlled comparison and honest generalization protocol, not simply another high tile-level accuracy on SDNET2018.

The current protocol already contains the main needed elements:

- SDNET2018 as the primary dataset, with all tiles from one source photo assigned to one split;
- tile-level development results labeled preliminary when parent IDs are unavailable;
- weighted binary cross-entropy with the positive weight computed from training data only;
- validation-only checkpoint and optional threshold selection;
- crack recall, F1, average precision, and balanced accuracy as primary outcomes;
- three fixed seeds, per-surface results, and three leave-one-surface-out rotations;
- parameters, latency, and peak memory alongside precision, specificity, ROC-AUC, and confusion matrices.

Those choices are consistent with the dataset imbalance and recent source-held-out and cross-dataset practice. The **go/no-go item** is the parent-photo mapping: confirm that it is documented and applied before describing test results as source-separated. If it cannot be recovered, keep development scores clearly preliminary and seek a separate source-level test collection rather than making a rigorous-sounding claim from a tile split.

## Search coverage and limitations

Searches for this note covered the SDNET2018 source paper and official record, source-image grouping and spatial-correlation evaluation, crack-classification metrics and imbalance, cross-dataset classification, systematic reviews, lightweight/edge reporting, and selected dataset papers or official repositories from 2025–2026. Sources were prioritized from journal/conference publishers, arXiv for clearly marked preprints, and official dataset repositories such as Zenodo.

This is a targeted evidence review, **not a claim that every paper or dataset in the domain has been found**. The domain includes concrete, asphalt pavement, masonry, bridge and building imagery, segmentation, detection, classification, severity assessment, and many proprietary datasets. Cross-paper score comparisons are not valid unless task, split, class prevalence, image resolution, training data, and evaluation conditions are aligned.

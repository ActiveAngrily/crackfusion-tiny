# Literature survey: compact CNN–Transformer concrete-crack classification

**Survey cutoff:** 6 October 2026\
**Paper scope:** binary concrete crack image classification using SDNET2018; compact local/global CNN–Transformer models; source-photo separation, cross-surface evaluation and efficiency.

This folder is the working literature corpus for the paper. The survey covers direct classifiers, architecture foundations, segmentation as adjacent work, dataset lineage, generalization, robustness, interpretability, deployment, and field reviews. Source-specific reading and access status appears in each workstream; see the [reading ledger](reading_ledger.md) and [cross-area synthesis](synthesis_and_implications.md) first. This is a traceable targeted survey, not a claim that every paper in the domain was retrieved or read in full.

## Survey files

| File | Coverage |
|---|---|
| [01 — Image-level crack classification](crack_classification.md) | Crack/no-crack and severity classifiers; direct hybrid prior art; source and metric caveats. |
| [02 — CNN–Transformer architectures](hybrid_architectures.md) | Primary architecture foundations and efficient/mobile hybrids. General-vision results are kept separate from crack evidence. |
| [03 — Detection and segmentation](crack_detection_segmentation.md) | Dense crack localization and segmentation as adjacent tasks, not classifier baselines. |
| [04 — Datasets and generalization](datasets_generalization.md) | Dataset provenance, split leakage, domain shift, metrics, threshold choice, and uncertainty. |
| [05 — Efficiency and deployment](efficiency_and_deployment.md) | Classifier compute, mobile/edge evidence, measurement quality, and reporting needs. |
| [06 — Reviews and research position](reviews_and_research_position.md) | Review screening, safe novelty boundaries, evidence quality, interpretability limits, and Zotero audit. |
| [07 — Reading ledger](reading_ledger.md) | Corpus index, access labels, source verification flags, and refresh items. |
| [08 — Cross-area synthesis](synthesis_and_implications.md) | What the surveyed evidence supports and how it constrains the paper and experiments. |
| [09 — Search completeness](search_completeness.md) | Search methods and limits; newly surfaced 2025–26 classifier candidates and follow-up searches. |
| [10 — Recent classification prior art](recent_classification_prior_art.md) | Close hybrid/classifier prior art, publication-date evidence, topology, split and access caveats. |
| [11 — Dataset lineage and benchmarking](dataset_lineage_and_benchmarking.md) | SDNET release audit status, source mapping limits, alternatives, duplicate audit protocol, and benchmark suitability. |
| [12 — Generalization, robustness and data efficiency](generalization_robustness_and_data_efficiency.md) | Grouped and cross-domain evidence, nuisance shifts, imbalance, adaptation, and label-efficiency experiments. |
| [13 — Interpretability, measurement and task extensions](interpretability_measurement_and_task_extensions.md) | Explanation faithfulness, mask localization, width metrology, severity labels, and evidence requirements. |
| [14 — Deployment, multimodal and temporal evidence](deployment_multimodal_and_temporal.md) | Platform measurement quality and temporal/video, 3D, thermal, RGB-D and multisensor task boundaries. |

## Main findings

- Crack classification is distinct from detection, pixel segmentation, severity grading, measurement, and structural diagnosis. Results across these tasks are not interchangeable.
- CNN–Transformer crack classifiers, parallel local/global branches, and adaptive fusion already exist. The March 2026 EfficientCrackFusion preprint is a direct binary-classification counterexample to broad “first hybrid” claims; its reported parameter/FLOP totals conflict with its stated ViT-Base backbone and should not be treated as validated efficiency evidence.
- Recent direct classifier comparators also include Sait et al.'s concrete/asphalt local/global model, frozen-CLIP classification on SDNET2018, an attention-enhanced ConvNeXt, and lightweight MobileNetV3 attention work. Task labels, dataset overlap, splits, and full-text availability differ; see [09](search_completeness.md) and [10](recent_classification_prior_art.md).
- SDNET2018's 56,092 tiles derive from 230 source photographs. The official file endpoint could not be inspected in this survey; a complete authoritative tile-to-parent mapping has not been verified. Source-photo-held-out results therefore remain unsupported.
- Cross-surface and external-dataset evaluation address different, composite shifts. Direct studies report substantial cross-collection drops, but the most striking target result has only 118 patches from three photos. Headline scores from random tile splits are not comparable with source-held-out results.
- Explanation maps do not validate pixel localization, physical width, severity, or structural risk. Those claims require the corresponding masks, calibration/reference measurements, operational labels, and grouped validation.
- Parameter count does not establish speed or deployment readiness. Platform-specific latency, memory, energy, batch, precision, runtime, and timing boundaries matter; see [05](efficiency_and_deployment.md) and [14](deployment_multimodal_and_temporal.md).
- CrackNeXt and DBD-KD remain date/full-text watchlist items. Multiple other sources are abstract-only or partial-text; those limits are marked. The corpus is broad and traceable, but not a registered database census or a claim that every paper was read in full.

## Project references

- Prior project notes: [`Literature Review/`](earlier_review_index.md)
- Zotero metadata export: [`sources/zotero_snapshot.json`](../references/zotero_snapshot.json)
- Current protocol: [`docs/experimental_protocol.md`](../../planning/experimental_protocol.md)
- Implemented model: [`src/crackfusion_tiny.py`](../../../notebooks/03_crackfusion_train.ipynb)

Report author-reported values with their source, task and split. Do not imply source-independent generalization, fusion benefit, edge readiness, localization, or calibrated severity until the corresponding data and experiments support those claims.

# Reading ledger and source verification

**Survey cutoff:** 6 October 2026. This ledger indexes the source work captured in files `01`–`06` and the second-pass workstreams `09`–`14`; the source-specific tables are authoritative for exact claims and each paper's access status. The survey is broad and targeted, not a registered database census, and not every candidate was available in full text.

## Workstream index

| File | Evidence area | What is tracked there |
|---|---|---|
| [01 — Image-level crack classification](crack_classification.md) | Crack presence, type, severity; SDNET2018; crack-specific hybrid classifiers | Paper-by-paper architecture, dataset, split caveats, results, and full-text/abstract access status. |
| [02 — CNN–Transformer architectures](hybrid_architectures.md) | Vision architecture foundations and efficient/mobile hybrids | Primary-source topology notes, general-vision limits, search trail, and design relevance. |
| [03 — Detection and segmentation](crack_detection_segmentation.md) | Pixel-level masks, salient maps, dense prediction, deployment-adjacent models | Task boundary, recent model table, comparison limits, and primary/abstract access status. |
| [04 — Datasets and generalization](datasets_generalization.md) | Dataset lineage, split leakage, domain shift, metrics and uncertainty | Provenance evidence, cross-source studies, source-level grouping requirements, and project gates. |
| [05 — Efficiency and deployment](efficiency_and_deployment.md) | Classifier compute, mobile/edge deployment, timing quality | Device and timing evidence, incomparable headline figures, reporting checklist, and access status. |
| [06 — Reviews and paper positioning](reviews_and_research_position.md) | Reviews, interpretability, novelty boundary, Zotero audit | Review screening, cutoff checks, evidence quality, safe claims, and metadata limitations. |
| [09 — Search completeness](search_completeness.md) | Search method and recent candidates | Second-pass queries, database/export limits, direct classifiers, and closure steps. |
| [10 — Recent classification prior art](recent_classification_prior_art.md) | Close 2025–26 classifiers and hybrids | Topology, dates, split evidence, access, and novelty consequences. |
| [11 — Dataset lineage and benchmarking](dataset_lineage_and_benchmarking.md) | Dataset provenance and benchmark fit | SDNET archive access limits, mapping status, alternatives, overlap protocol, and split claims. |
| [12 — Generalization, robustness and data efficiency](generalization_robustness_and_data_efficiency.md) | Domain shift, nuisance variation, imbalance | Direct classification evidence versus adjacent-task evidence and group-aware experiments. |
| [13 — Interpretability, measurement and task extensions](interpretability_measurement_and_task_extensions.md) | Explanations, masks, width, severity | Faithfulness limits and evidence required for expanded output claims. |
| [14 — Deployment, multimodal and temporal evidence](deployment_multimodal_and_temporal.md) | Edge deployment, video, 3D and multiple sensors | Device-measurement quality and task boundaries for temporal, geometric, thermal and fused sensing. |

## Source-access labels

- **Full text read:** the complete article or preprint was available and its relevant methods/results sections were read. It does not mean every appendix or reference was independently rechecked unless stated.
- **Partial full text / indexed tables:** the primary publisher text or PDF was searchable, but direct access or complete linear inspection was blocked. Use only the verified sections and tables described in the workstream note.
- **Abstract or metadata only:** title, abstract, highlights, bibliographic record, dataset-owner record, or a search excerpt was accessible; method details and unexposed numbers remain unverified.
- **Inherited project source:** earlier project literature notes document the source and its conclusions. The current workstream says when it extended or did not re-read that paper.
- **Preprint:** a primary author manuscript, not automatically peer-reviewed. The relevant entries identify preprint status.

These labels are intentionally conservative. A publisher page or indexed excerpt is not counted as a full-text read simply because it reproduces the abstract or a result table.

## Cross-workstream reading record

### Crack classification and architecture

The classification file records direct task sources and access state for Kim et al. (2018), SDNET2018, CCTNet (2024), CSW-S (2024), 2025 Swin/EFRB and severity work, 2026 attention/Transformer classifiers, AttXNet v2, and date-ambiguous CrackNeXt and DBD-KD. The second pass adds EfficientCrackFusion (a pre-cutoff parallel local/global hybrid preprint), Sait et al. (2026), frozen-CLIP SDNET classification, attention-enhanced ConvNeXt, and lightweight/threshold candidates. The architecture file covers ResNet, ViT/DeiT, Swin, CvT, Conformer, CoAtNet, CMT, MobileViT, Mobile-Former, FastViT, EfficientViT, MobileNetV4, SHViT, iFormer, TinyNeXt and BHViT. It distinguishes primary-paper evidence from general-vision transfer lessons.

### Localization and segmentation

The segmentation file tracks the recent mask/saliency models and separates dense prediction from the project's image-level labels. It flags papers where only an abstract, indexed publisher text, or inherited project review was available. Older segmentation hybrids are indexed in the earlier project review linked there; their metrics are not imported as classifier results.

### Data and evaluation

The dataset files record SDNET2018, CCIC/CCI, Historical-Crack18-19, masonry and historic-stone examples, plus road/video and composite datasets used only as adjacent evidence. They track original-source counts, available lineage, direct domain-transfer studies, split units, class prevalence, threshold choice and cluster-level uncertainty. The second pass read visible official SDNET metadata, but the archive file endpoint returned 403; it found no verified complete tile-parent mapping while leaving archive contents unverified. No lineage is inferred from filenames.

### Efficiency and review-level sources

The efficiency file distinguishes measured platform work, author-reported abstracts and non-comparable segmentation throughput. The reviews file lists the review articles included at cutoff, interpretability foundations, and the 24-record Zotero metadata audit. The prior project synthesis says 22 records were previously read in full; the exported JSON alone does not preserve enough attachment/note detail to independently certify that statement record by record.

The follow-up finds a direct cross-collection classification warning, a source-photo-grouped SDNET split precedent, and a contrasting tile-random split with acknowledged spatial correlation; the cross-collection target has only three source photos. Robustness corruption, few-shot and self-supervised evidence remains sparse or belongs to segmentation/detection, so those results are kept as experiment leads rather than classifier evidence. Interpretability sources distinguish classifier explanations from masks; width/severity work requires calibration and operational labels. A UAV/TinyML classifier supplies direct deployment precedent, but key figures are abstract-level here; video, thermal, RGB-D and point-cloud studies are recorded as adjacent system/task evidence. See [12](generalization_robustness_and_data_efficiency.md), [13](interpretability_measurement_and_task_extensions.md), and [14](deployment_multimodal_and_temporal.md).

## Verification flags to carry into the manuscript

1. **CCTNet (2024):** its SDNET2018 Table 3 prints five fold accuracies whose arithmetic mean is 98.90%, but labels the average as 98.04%. The paper's own table is internally inconsistent; neither value should be silently promoted as a validated summary. See [01](crack_classification.md).
2. **AttXNet (2026 preprint):** full arXiv HTML v2 was read. Its SDNET tile-level split does not group by source photograph, its limitations acknowledge spatial correlation, and 825 FPS refers to a ground-station-assisted batch patch workflow. See [01](crack_classification.md), [04](datasets_generalization.md), and [05](efficiency_and_deployment.md).
3. **EfficientCrackFusion (2026 preprint):** its 18 March author preprint is direct pre-cutoff prior art for parallel CNN/Transformer crack classification and adaptive local/global fusion. Full text was read, but 12.8M reported parameters conflict with the stated ViT-Base branch; visual-hash clusters do not establish parent-structure independence. See [10](recent_classification_prior_art.md).
4. **Sait et al. (2026):** authorship in [09](search_completeness.md) was corrected to match the Nature record. The full article was read for architecture and dataset descriptions, but source overlap and all result tables were not audited. Do not attribute the paper to Ansary et al.
5. **CrackNeXt:** the publisher's volume listing says December 2026, while ResearchGate reports June 2026; the online-first date could not be verified from the publisher. Keep it in the prior-art watchlist and resolve the date before making a time-bounded novelty claim. Its abstract is not a full-text review. See [01](crack_classification.md), [06](reviews_and_research_position.md), and [10](recent_classification_prior_art.md).
6. **DBD-KD:** the publisher lists a November 2026 issue, while its DOI month and a secondary 19 September listing suggest possible September online availability. The publisher's online-first date and full text were not verified; keep cutoff status and exact inference topology unresolved. See [01](crack_classification.md), [06](reviews_and_research_position.md), and [10](recent_classification_prior_art.md).
7. **CCI/CCID:** the official Mendeley V1 record says 2,000 images; a 2025 cross-dataset paper says 2,126. The archive/version identity must be resolved before citing a fixed count or using it as an external test. See [04](datasets_generalization.md).
8. **SDNET source map:** the published dataset paper reports 230 source photographs, but the official archive could not be inspected and no complete verified tile-to-parent mapping was found. Whether the downloadable files contain relevant lineage remains unverified; source-separated results are unsupported until resolved. See [04](datasets_generalization.md) and [11](dataset_lineage_and_benchmarking.md).
9. **Cross-collection result:** de Almeida et al. report >99% source accuracy and roughly 54% on an Itaipu target set of 118 patches from three photos. This is a transfer warning, not a population-level estimate. See [12](generalization_robustness_and_data_efficiency.md).
10. **Access limits:** multiple publisher pages returned 403/429, paywall, or bot checks. Each note states whether it used full text, partial/indexed text, abstract, or metadata; do not turn limited access into a full-text claim.

## Search coverage and next reading pass

Searches were conducted on 6 October 2026 across publisher and DOI records, open-access full texts, conference proceedings, arXiv, dataset-owner repositories and citation/title searches. Query concepts are recorded in each workstream. The pass was broad across classification, hybrid architectures, segmentation, datasets/generalization, robustness, interpretability, measurement, deployment and reviews, but it was not a systematic Scopus/Web of Science/IEEE Xplore export with duplicate-screening flow. Subscription-only proceedings, non-English papers, late-indexed 2026 studies, and papers not retrieved by targeted terms may be missing.

Before manuscript submission, refresh the cutoff search; verify CrackNeXt's and DBD-KD's online-first dates and primary texts; inspect abstract-only classifier candidates; and run reproducible database exports and citation chaining around 2025–2026 compact crack classifiers. Before experiments, inspect the official SDNET archive and prioritize an author-verified parent map. This reading list is a traceable working corpus, not a completeness certificate.

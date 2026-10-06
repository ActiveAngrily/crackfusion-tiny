# Crack datasets, provenance, split leakage, and generalization

**Survey date:** 6 October 2026\
**Scope:** crack image classification datasets, source provenance, split design, domain shift, class imbalance, evaluation metrics, threshold selection, and uncertainty. Related detection/segmentation datasets appear only where their sampling structure informs classification. This is a targeted evidence review, not a claim to have found every paper or dataset.

## Main conclusions

1. SDNET2018 is **56,092 tiles from 230 original photographs**, not 56,092 independent acquisitions. The source paper reports 54 deck, 72 wall, and 104 pavement photographs, with 8,484 crack and 47,608 non-crack tiles.
2. The project has not yet established a complete tile-to-parent-photo mapping. Its data-audit notebook leaves `parent_id` blank unless a documented map is supplied and labels the current 3,600-image subset `tile_development_only`. Therefore no current project result can be called source-photo-held-out.
3. A tile-random split, a parent-photo split, a held-out surface split, and an external-dataset test support different generalization claims. Counts at tile level can substantially overstate the number of independent source examples.
4. The current leave-one-surface-out (LOSO) protocol is useful as a **composite held-out-surface transfer test**. It does not isolate a causal “surface effect”: material, structure type, geography, camera/capture conditions, and prevalence may shift together. There are only three target surface categories.
5. Two recent SDNET papers illustrate the split distinction directly: Zhang et al. (2026) assign all patches from a parent photo to a single partition; Li et al. (2026, AttX-Net preprint) use a stratified tile-level split and explicitly acknowledge residual spatial correlation.
6. Report crack-sensitive metrics, preserve natural test prevalence, choose checkpoint and threshold on validation only, and calculate test uncertainty at the independent source-group level. Variation over three training seeds is not uncertainty over new photographs or structures.

## Dataset and provenance evidence

| Dataset | Direct evidence and provenance | Relevance / caveat |
|---|---|---|
| **SDNET2018** | Dorafshan, Thomas & Maguire, 2018, *Data in Brief*, [doi:10.1016/j.dib.2018.11.015](https://doi.org/10.1016/j.dib.2018.11.015); [official USU dataset record](https://digitalcommons.usu.edu/all_datasets/48/). The data article reports 230 photographs (54 decks, 72 walls, 104 pavements), divided into >56,000 256×256 tiles. It gives 8,484 cracked and 47,608 uncracked tiles. | Primary benchmark. The 230 source images need not represent 230 independent structures/sites. The article’s count is not itself a tile-to-photo lookup table. |
| **CCIC / CCiC (METU)** | Özgenel & Sorguç, 2018, [ISARC paper](https://doi.org/10.22260/ISARC2018/0094); [Mendeley Data](https://data.mendeley.net/datasets/5y9wdsg2zt/1); further dataset/split detail in the full-text domain adaptation paper [doi:10.1007/s43503-022-00008-6](https://doi.org/10.1007/s43503-022-00008-6). The latter describes 40,000 balanced 227×227 patches cropped from 458 3024×4032 METU photographs and a patch-level 70/20/10 partition. | Candidate external concrete source, but balance and acquisition differ from SDNET. The patch split is not evidence of source-photo separation. Confirm whether the exact archive/version includes parent mapping before use. |
| **CCI / CCID (Gümüşhane)** | [Official Mendeley CCID V1 record](https://data.mendeley.com/datasets/fgjy2s3nk7/1) says 2,000 smartphone images from Gümüşhane, Turkey. Rashid et al. (2025), [doi:10.1515/jmbm-2025-0074](https://doi.org/10.1515/jmbm-2025-0074), describes CCI as 2,126 photographs. | Different collection from CCIC. The count mismatch may be a version or packaging difference; resolve exact ID/version before citing or testing. The official V1 record does not specify repeated-view grouping. |
| **Historical-Crack18-19 / HBC** | Elhariri et al., 2022, *Data in Brief*, [doi:10.1016/j.dib.2022.107865](https://doi.org/10.1016/j.dib.2022.107865); [Mendeley record](https://data.mendeley.com/datasets/xfk99kpmj9/1). About 3,886 labelled 256×256 patches (757 cracked, 3,139 intact) from about 40 raw photographs at one historic Cairo mosque. | Good example of a large tile count from few sources. Not representative of many historic buildings; group patches by source photo. |
| **Masonry** | Heller et al., 2021, *Sensors*, [doi:10.3390/s21144929](https://doi.org/10.3390/s21144929); dataset [Zenodo doi:10.5281/zenodo.5108846](https://doi.org/10.5281/zenodo.5108846). The study describes 2,542 labelled laboratory patches, with 1,068 clear crack/uncracked cases used for supervised learning, and separately tests internet imagery. Hamburg aerial masonry data are described in the [CNR DHeLO record](https://chloe.cnr.it/s/DHeLO/item/5130): 834 original high-resolution images were tiled into >350k candidates, then filtered to ~40k. | Different material and task context. Lab↔internet transfer is relevant; distinguish it from random within-source testing. Preserve source/site identities. |
| **CRACK-CH historic stone masonry** | Agrafiotis et al., 2023 preprint, [arXiv:2303.17989](https://arxiv.org/abs/2303.17989); [Zenodo doi:10.5281/zenodo.6516913](https://doi.org/10.5281/zenodo.6516913). Repository describes 224×224 crack/no-crack patches from HYPERION sites Naillac and St. Nikolaos Fort. | Useful heritage/material shift example. The Zenodo narrative also describes a Roman bridge while its concise source description names two sites; inspect the actual archive/site metadata before use. Preprint, not a peer-reviewed benchmark standard. |
| **Attain (2025)** | Data in Brief, [doi:10.1016/j.dib.2025.111715](https://doi.org/10.1016/j.dib.2025.111715); [Mendeley doi:10.17632/nykrzdm74f.1](https://doi.org/10.17632/nykrzdm74f.1). 2,293 images from 20 hours of vehicle video, 19,761 distress instances, ten classes, severity labels; windshield-mounted smartphones. | Road detection/severity, not direct concrete tile classification. Group by source video/drive/location to avoid temporal near-neighbor leakage. |
| **PaveTrack (2025)** | *Scientific Data*, [doi:10.1038/s41597-025-05748-5](https://doi.org/10.1038/s41597-025-05748-5); [Science DataBank doi:10.57760/sciencedb.20383](https://doi.org/10.57760/sciencedb.20383). Provides pavement distress detection images and a separate repeated-defect tracking/matching subset. | Useful future temporal/pavement work. The paper describes 70/15/15 stratification for the detector set; that is not, by itself, source-held-out. Keep tracked defect/time sequences together. |
| **StructDamage (2026)** | Ijaz et al., [arXiv:2603.10484](https://arxiv.org/abs/2603.10484), preprint: ~78,093 images assembled and relabelled from 32 public datasets across concrete, road, masonry, bridges, and historic buildings. | A composite benchmark can overlap SDNET, CCIC, or derivatives. Audit source roster, deduplication, lineage retention, split manifests, and version before using it as an “external” test. Large total count does not guarantee many independent sources. |

### SDNET counts and the unresolved mapping

The original SDNET data paper is the preferred source for the source-photo and tile counts. Arithmetic from its class totals gives crack prevalence 8,484/56,092 = **15.1%** and an always-negative accuracy of **84.9%**. By surface: deck 2,025/13,620 = 14.9%; wall 3,851/18,138 = 21.2%; pavement 2,608/24,334 = 10.7%.

The project audit notebook explicitly says the six public class folders do not prove which source photograph produced each tile. It accepts a parent ID only from a documented mapping; otherwise IDs remain blank and the research split is unassigned. The saved development bundle has 3,600 images with blank parent IDs. Thus published knowledge that there were 230 originals does not satisfy the project’s lineage gate. Exact hashes detect byte-identical duplicates, not sibling tiles from one photo; visual similarity can flag candidates but is not provenance evidence without validation.

## What each split can establish

| Split | Held-out unit | Claim supported | Main limitation |
|---|---|---|---|
| **Tile-random / patch-random** | Individual patches | Performance on more tiles from the same collection. | Nearby tiles can share concrete texture, lighting, camera response, and crack geometry; overlapping or adjacent crops can make test tiles close neighbors of training tiles. Tile count overstates independent evidence. |
| **Source-photo-held-out** | All tiles from an original photograph remain in one partition | Transfer to unseen photographs under broadly similar collection conditions. | Does not establish transfer to unseen structure, site, camera, or campaign if several photos come from one structure/campaign. Requires complete traceable parent map. |
| **Surface-held-out (LOSO)** | One surface category excluded from train and validation and used for test | Transfer to one unseen SDNET surface category; report each of the three rotations. | Surface is confounded with structure context, capture process, prevalence, and possibly geography. Three categories mean only three target domains. Parent grouping is still needed inside training surfaces. |
| **External-dataset test** | Separately collected dataset/source | Transfer to a different collection/acquisition/label pipeline. | Material, camera, scale, label rule, prevalence and selection may all differ. Check source overlap and compatible labels. |
| **Site/structure/inspection-held-out** | Entire bridge/building/site, inspection visit or video sequence | Stronger evidence for transfer beyond sampled structures or acquisition passes. | Requires metadata and enough independent sites; one external site is a case study, not a broad population guarantee. |

The project’s three LOSO rotations are therefore a useful **composite shift evaluation**, not a controlled causal estimate of the effect of surface material alone. Phrase results as held-out-surface transfer and report all rotations separately. A more deployment-relevant design combines source-photo grouping in training domains with a separately collected site/structure test.

## Direct studies on split choice and generalization

### Recent SDNET split disclosures

- **Zhang et al. (2026), TinyML pipeline for efficient crack classification in UAV-based structural health inspections**, *Scientific Reports*, [doi:10.1038/s41598-026-43534-4](https://doi.org/10.1038/s41598-026-43534-4). The paper explicitly assigns all patches from one original high-resolution photograph to one train/validation/test partition to reduce spatial correlation. It uses an 8:1:1 split on a balanced 16,800-patch SDNET subset. This is direct source-photo split precedent. It is not full-data natural-prevalence evaluation; its focus is preprocessing, compression and MCU deployment.
- **Li et al. (2026), Robust Lightweight Crack Classification for Real-Time UAV Bridge Inspection (AttX-Net)**, [arXiv:2604.27617v2](https://arxiv.org/abs/2604.27617), preprint. It uses SDNET deck tiles and a stratified 70/15/15 split. In its limitations it says tile-level splitting may retain spatial correlations among visually similar regions and recommends structure/location/inspection-region splitting when metadata exists. The split is not source-photo-held-out. The reported speed is for a ground-station pipeline; it does not demonstrate onboard UAV inference. The preprint says code and split scripts will be released upon publication, so reproducibility of the current split was not independently confirmed here.
- **Dorafshan et al. (2018)** provides dataset counts and acquisition context, not a per-tile parent map or a universal split recommendation. Repeated use of SDNET in later studies does not prove independent source splits.

### Direct cross-source/cross-domain evidence

- **de Almeida et al. (2022), Domain adversarial training for classification of cracking in images of concrete surfaces**, *AI in Civil Engineering*, [doi:10.1007/s43503-022-00008-6](https://doi.org/10.1007/s43503-022-00008-6). Trains on CCiC (40k patches from 458 METU photos) and evaluates transfer to Itaipu Dam images: 294 labelled patches cropped from three large target photos, with 176 train / 118 test in its target split. Source-only model accuracy is reported above 99% on the source test but about 54% on the Itaipu target test. This is direct evidence that high within-collection scores do not establish transfer. Limits: target test is small and comes from only three photos; adaptation uses unlabeled target data and a target-only comparison uses labels, so distinguish zero-shot source-only results from adaptation. Accuracy alone is insufficient to judge practical alert burden.
- **Rashid et al. (2025), Cross-dataset evaluation of deep learning models for crack classification in structural surfaces**, *Journal of Municipal Economy*, [doi:10.1515/jmbm-2025-0074](https://doi.org/10.1515/jmbm-2025-0074). Evaluates CNN, ResNet50, LSTM and VGG16 across SDNET2018, SCD/CCIC, CPC, CDIBM, CCI and HBC. It reports self-test accuracies up to 100% on some collections and large cross-test drops (e.g. SCD-trained models on CDIBM). Its own method describes stratified 70/15/15 per-dataset splits, with no documented source-photo/site groups, and reports single runs. It resizes to 224×224 and applies ImageNet normalization. Treat transfer patterns as evidence to run cross-domain tests, not as a source-independent performance estimate or an architecture causal comparison. Multiple domain attributes change together, so the paper does not isolate resolution, texture, camera, or label effects.
- **Heller et al. (2021)**, above, tests laboratory masonry against internet-collected imagery and reports asymmetric transfer by direction. It is relevant to domain shift but is not the same material or binary concrete task. A→B and B→A should not be assumed equivalent.

These studies establish a rationale for source and domain evaluation; they do not supply one universally accepted “generalization score” for crack classifiers.

## Imbalance, metrics, thresholds and uncertainty

### Imbalance and metric choice

SDNET’s majority-class baseline is 84.9% accuracy with zero crack recall. Keep the test set at its natural prevalence; balancing the test set changes precision and its operational meaning. A balanced training subset or weighted loss is a training choice, not a reason to report test precision as if it reflected field prevalence.

- Report crack-positive **recall, precision, F1**, confusion matrix and specificity at a stated threshold. Recall measures missed crack examples; precision reflects alert burden. State positive class explicitly.
- Report **average precision (AP)** or a precision–recall curve with test prevalence. AP depends on prevalence and is not necessarily trapezoidal PR-AUC. Keep naming and implementation consistent.
- Include **balanced accuracy** and ROC-AUC as additional views. Neither replaces threshold-specific precision/recall, and ROC-AUC does not convey prevalence-dependent alert precision.
- If probability outputs are interpreted as risk, add calibration diagnostics (e.g. Brier score or reliability plot); classification metrics alone do not establish calibrated probabilities.

### Threshold and model-selection safeguards

1. Predeclare the main threshold (current protocol defaults to 0.5), or choose it from a grouped validation set with a named objective/constraint. Freeze it before test evaluation.
2. Use training/validation only for checkpoint, architecture/hyperparameter, class-weight/sampling and threshold decisions. In LOSO, never inspect held-out-surface labels or outcomes for epoch, threshold, transform or variant selection.
3. Evaluate every held-out surface at the same predeclared operating point. AP/ROC-AUC can describe threshold-independent ranking; any threshold adaptation must state which source validation data chose it.
4. Persist per-image probabilities and verified parent IDs before test scoring. The audit found an old training metric call that ignored a configured threshold; the completed run used 0.5 and was unaffected, but fix shared callers before a threshold study.

### Uncertainty at the acquisition-group level

Tiles sharing a photo are correlated. For a source-photo-held-out test, resample **source photographs**, carrying all their tiles and predictions together. For model differences, use paired cluster resampling over the same parent IDs for each model. If the target claim concerns new structures or campaigns, the higher-level sampling cluster should be site/structure/campaign, not the patch or perhaps even the photo.

Report group counts and make the estimand explicit: a tile-weighted metric gives more weight to photographs with more patches; a photo-weighted summary gives equal weight to each source. With 230 SDNET photos and only three surface categories, neither a bootstrap interval nor a standard deviation should be presented as a guarantee over all concrete infrastructure. Three fixed seeds estimate optimization variation conditional on the same split; they are not three independent datasets and do not form a confidence interval over new source photos. Show seed results separately from source-cluster uncertainty. Few top-level sites can make cluster intervals unstable; disclose that limit.

Method reference: Field & Welsh, “Bootstrapping clustered data,” *JRSS B* 69(3), 369–390 (2007), [doi:10.1111/j.1467-9868.2007.00593.x](https://doi.org/10.1111/j.1467-9868.2007.00593.x). Resampling should reflect the independent clusters. This is general statistical guidance, not crack-specific evidence.

## Implications and project gates

The protocol’s question—whether explicit lightweight local/global fusion helps under source-separated and cross-surface evaluation—is defensible if results respect grouping and qualify claims.

1. **Resolve SDNET provenance first.** Obtain a complete documented tile→source-photo map and record the mapping source and coverage. If not recoverable, retain the current tile subset as pipeline development and do not call its split source-separated.
2. **Split before training.** Keep each parent photo in one partition; audit exact duplicates across partitions. For LOSO, make grouped train/validation splits within the two training surfaces and seal the third surface for final scoring.
3. **Freeze choices before test.** Fix model/hyperparameters/checkpoint rule/threshold on validation. Do not tune against held-out surface or external test. Explain LOSO as composite shift.
4. **Keep test prevalence natural.** Report per-surface n and class counts, crack recall/precision/F1, AP, balanced accuracy, specificity, ROC-AUC and confusion matrix. Report all seeds, distinguishing seed spread from source-group uncertainty.
5. **Use paired cluster uncertainty.** For within-SDNET comparisons, bootstrap parent IDs, not tiles. Treat three LOSO surfaces as three domain cases. Add independently collected site data only when label semantics, source overlap, and acquisition unit are auditable.
6. **Keep adjacent tasks adjacent.** Attain, PaveTrack, CRACK-CH and severity/segmentation datasets are not direct binary concrete classification tests without a task change and explicit label harmonization.

## Search log and full-text/access status

Searches on 6 October 2026 covered SDNET2018 source article and official record; CCIC/CCI archives; parent-photo, tile-level and source-level split disclosures; direct CCiC→Itaipu transfer; cross-dataset classification; masonry, historic-building and bridge datasets; and selected 2025–2026 road, temporal, and composite datasets. Primary journal papers, author preprints and dataset-owner repositories were preferred. Secondary reviews/tables were used as leads, not sole evidence for counts or dataset identity.

| Source | Access/read status | Limitations noted |
|---|---|---|
| Dorafshan et al. 2018 SDNET2018 | Full open article text read (counts, capture and dataset description); official USU record checked. | Did not identify a per-tile source mapping in the described release; project archive folders do not establish one. |
| Özgenel & Sorguç 2018 CCIC | Official data record inspected; parent count and split details cross-checked against full 2022 DA-Crack article. | Exact archive not downloaded in this review; parent map availability/version remains unknown. |
| de Almeida et al. 2022 DA-Crack | Full open article text read for both datasets, splits, transfer method and results. | Small target set; accuracy-only result limits operational interpretation. |
| Rashid et al. 2025 cross-dataset paper | Full 29-page PDF read for dataset descriptions, split/preprocessing, metrics and transfer results. | Patch-stratified split, no seed repeats, and mixed datasets limit inference. |
| Zhang et al. 2026 TinyML | Journal full-text search excerpt and PDF passages read for dataset split and deployment method. | Balanced subset, not natural prevalence; focus is embedded deployment. |
| Li et al. 2026 AttX-Net | Full arXiv HTML v2 read for SDNET split, limitations and conclusions. | Preprint; code/splits were stated to be released upon publication. |
| Elhariri et al. 2022 HBC | Full open article text read. | One mosque and ~40 raw photographs. |
| Heller et al. 2021 masonry | Full open article text and data statement read. | Controlled masonry task and external internet images differ from SDNET concrete classification. |
| CRACK-CH 2023 | Official Zenodo record read; linked arXiv paper identified, not fully audited here. | Site descriptions are ambiguous; inspect archive metadata. |
| Attain 2025 | Data article specification and official Mendeley record read. | Video/drive split protocol not established from accessible specification. |
| PaveTrack 2025 | Scientific Data article passages on dataset subsets/splits read. | Adjacent detection/tracking task. |
| StructDamage 2026 | arXiv full-text portions on collection scope/construction read; preprint status confirmed. | Full source overlap, deduplication and grouping audit remains necessary. |
| CCI/CCID | Official Mendeley V1 record and 2025 study compared. | Conflicting counts: 2,000 vs 2,126; exact version identity unresolved. |
| Field & Welsh 2007 | DOI/bibliographic record checked. | General clustered-data method, not crack-specific. |

## Evidence boundary

This note supports a source-aware evaluation design and records known provenance questions. It does not download/checksum every external archive, audit licenses, inspect all papers in the field, or quantify how much tile leakage changes any model score. Correlation makes tile-random estimates potentially optimistic, but the magnitude must be measured using matched source-aware splits. New preprints and composite datasets need independent source-roster, split-manifest, and code checks before benchmark use.

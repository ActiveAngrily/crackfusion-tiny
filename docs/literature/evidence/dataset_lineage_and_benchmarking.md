# Dataset lineage and benchmarking review

## Decision

**Do not describe a random tile-level SDNET2018 split as source-independent evaluation.** The official record and dataset paper establish 230 high-resolution captures and 56,092 released 256×256 image patches, but the primary materials surfaced in this review do not establish that the 230 parent captures, their files, a tile-to-parent manifest, or tile coordinates are included in the release. No verified public mapping from every released tile to its parent was found. Reconstruction from tile pixels may recover some local relationships, but without a ground-truth manifest it is not a defensible substitute for provenance.

Until author-provided originals or a verified manifest are obtained, use SDNET2018 as a patch benchmark with an explicit leakage limitation, report train/test exact and near-duplicate checks, and keep its result separate from source-group generalization claims. For rigorous group evaluation, prefer a dataset that publishes parent images plus patch mapping/splits, or collect independent structures and hold them out as groups.

## SDNET2018 primary record and package

The [USU Digital Commons record](https://digitalcommons.usu.edu/all_datasets/48/) identifies the dataset, authors, date, CC BY 4.0 license, checksum (`677411e784f194422c90f52d9ed0d7c6`), and two downloadable files: `ReadMe_SDNET2018.txt` (4 kB) and `SDNET2018.zip` (515,903 kB). It says 230 images were captured (54 bridge decks, 72 walls, 104 pavements), each segmented into 256×256 subimages; each patch is labeled cracked (`C`) or uncracked (`U`). The repository page labels file formats `.jpeg, .txt`. The browser could read the metadata but the file endpoint returned HTTP 403 during this review, so archive contents were **not independently inspected here**.

The [dataset paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC6247444/) reports 56,092 JPEG patches, split into D/P/W domains and C/U folders; it also says the image files are unchanged apart from segmentation. Its cited capture process used a 16 MP Nikon camera. It does not publish tile coordinates or a crop-to-parent mapping in the article. The paper and record describe source images as the inputs to segmentation; this does **not** prove source files are present in the downloadable archive.

### Provenance findings

| Question | Evidence-based status |
|---|---|
| Are the camera originals known to exist? | Yes: primary record/paper describe 230 captures. |
| Are those originals included in the public release? | **Unverified / not established.** The public page describes 56k subimages; file access blocked inspection. |
| Is there an official tile-to-parent CSV, coordinate index, or original-image list? | **Not found** in the article or visible official record metadata. The downloadable readme/zip could not be inspected in this review. |
| Is there a proven community mapping for all tiles? | **Not found.** Community notebooks and repos commonly download the official patch folders or create random splits; that is not lineage evidence. |
| Can parent mapping be reconstructed from image pixels? | Potentially partial. Exact duplicates, near duplicates, and matching neighboring edges may identify candidate relationships. This does not prove full parent identity, source coordinates, completeness, or absence of missed links. |
| Can source images be reconstructed by stitching all tiles? | Not rigorously on evidence available. A valid mosaic requires tile coordinates/orientation and proof of complete coverage. Unmatched patch adjacency or a visually plausible mosaic is insufficient. |

The original paper's folder labels identify material/location class (`D`, `P`, `W`) and crack status (`C`, `U`), not parent identities. A filename pattern or sorting order should not be treated as source order absent a documented guarantee. Later papers that say they split at the high-resolution-image level are not proof that they publish the mapping or that the procedure is independently reproducible; ask for their manifests and source artifact.

### Duplicate and leakage audit

No released-archive-wide duplicate scan or cross-dataset overlap scan was run in this research review; it therefore makes no claim about actual duplicate counts or whether SDNET2018 overlaps CCIC, BCD, or compiled benchmarks. Shared concrete surfaces across independently curated collections are plausible, and resized/cropped copies can evade simple file hashes. The next dataset audit should:

1. Record archive/version, retrieval date, official checksum, all paths, dimensions, labels, and SHA-256 of each decoded pixel array and original file bytes.
2. Find exact duplicates across labels, subsets, and external datasets; inspect conflicts rather than silently resolving them.
3. Generate perceptual-hash and local-feature candidate pairs, manually review borderline pairs, and report thresholds and counts. A candidate similarity score is not itself proof of shared parentage.
4. Search for crop adjacency through edge overlap/registration, and cluster candidate same-parent tiles only as a **provisional** grouping. Validate a sample against source originals or author manifest before making source-group claims.
5. Freeze all dedup decisions before splitting. Keep all confirmed same-parent tiles and exact/near duplicates in one partition. Publish image IDs, hashes, grouping rationale, and split seed.

Duplicate detection can find direct copies and some transformed overlaps; it cannot rule out spatial leakage between visually distinct crops from one large concrete surface. Tile-level splits remain potentially optimistic even after image-file duplicates are removed.

## Related classification datasets and auditability

| Dataset | Primary record / access | Lineage and label facts | License and auditability decision |
|---|---|---|---|
| **Concrete Crack Images for Classification (CCIC / METU)** | [Mendeley v1](https://data.mendeley.com/datasets/5y9wdsg2zt/1), [v2](https://data.mendeley.com/datasets/5y9wdsg2zt/2) | Record says 40,000 RGB patches (20k positive, 20k negative), 227×227, derived from 458 source images at 4032×3024; no random flip/rotation augmentation. The record reviewed does not state that the 458 originals or a patch-parent index are downloadable. | CC BY 4.0. Useful cross-domain patch classification set, but source-group evaluation is not auditable from stated metadata alone. Verify archive contents and ask authors for source mapping before claiming source-disjoint splits. |
| **Bridge Crack Dataset (BCD; common 6,069/6,070 patch release)** | [Original dataset paper](https://doi.org/10.3390/app9142867), [authors' GitHub](https://github.com/tjdxxhy/crack-detection) | Paper describes 2,068 original 1024×1024 UAV images, split into four 512×512 crops (8,272) then blurred images removed to leave 6,069. It is crack-only in the described original collection, so it is not a balanced crack/non-crack benchmark without a separately sourced negative class. | The GitHub README for the related DBCC release says non-commercial use; do not infer an unrestricted license for a repackaged BCD. Parent image lineage is described, but a verified parent map for every later patch distribution must be checked in the actual chosen archive. |
| **Bridge Crack Library (BCL)** | [Dataset paper record](https://trid.trb.org/View/1875180) | 11,000 256×256 pixel-labeled samples (5,769 nonsteel crack, 2,036 steel crack, 3,195 noise), collected across 50+ in-service bridges over two years. Stronger natural group unit is bridge/capture session, but a public group manifest was not established here. | Primary abstract establishes collection breadth and masks, not a redistribution license or a readily verified source-image manifest. Not currently recommended as a fully auditable source-group benchmark without locating the original release terms and grouping metadata. |
| **PAGG-Net Physically Aligned High-Resolution Concrete Crack Dataset** | [Zenodo record](https://zenodo.org/records/18010179) | Record describes 4224×5632 original images paired with pixel masks, multi-scale derived tiles, CSV tile mappings, MD5s, and image-level train/validation/test splits. | Excellent lineage design and a strong candidate for source-group segmentation/generalization protocol. Zenodo record states copyright by the author; no clear open license was displayed in the accessed metadata. Resolve reuse rights before adoption. |
| **Multi-temporal Crack Segmentation Dataset** | [Zenodo record](https://zenodo.org/records/15187675) | Record explicitly offers a high-resolution archive containing 25 parent images and masks plus a separate 128×128 patch archive with train/validation/test splits. Parent links are therefore auditable for its stated task. | Good example of a traceable parent-image split protocol. Check the record's license and task/domain fit before adopting; this is segmentation and multi-temporal material, not a drop-in classification replacement. |

Other large compilations (for example [OpenCrack](https://github.com/fadeevla/OpenCrack)) are useful discovery/index resources, but a consolidated roster is not automatically provenance proof. That project reports deduplication and explicitly distinguishes image-level sources including SDNET2018 and CCIC from mask datasets; any cross-benchmark overlap claim must be checked against source hashes and exact versions. Avoid treating broad web mirrors or repackaged folders as independent datasets without lineage and license checks.

## Reproducible next-step protocol

1. **Acquire and preserve source artifacts.** Download `ReadMe_SDNET2018.txt` and `SDNET2018.zip` only from the [official USU record](https://digitalcommons.usu.edu/all_datasets/48/); verify the published MD5, save retrieval time/version, and inventory archive paths and file types. Do not circulate a locally derived manifest until checked against the official files.
2. **Inspect the readme and archive before asserting availability.** Search for parent originals, a manifest, coordinates, capture IDs, and any checksum/list. If absent, send the corresponding authors a concise request for the 230 original images or an authoritative per-patch parent/coordinate index and permission/terms for its redistribution.
3. **Build a deterministic audit manifest.** One row per patch: release-relative path, SHA-256, decoded-pixel hash, domain, label, dimensions, exact duplicate cluster, near-duplicate candidate cluster, and evidence status. Preserve ambiguous/uncertain pairs rather than forcing a cluster.
4. **Choose split claims by evidence.** With author-confirmed parent mapping, group by parent capture (and, when available, structure/location) before stratifying. Without it, call any split “patch-random” or “deduplicated patch-level,” label it as potentially source-leaking, and do not present it as source-independent generalization. Use external datasets as separate tests only after a cross-dataset duplicate and license audit.
5. **Report what readers need to reproduce it.** Publish data version/checksum, exact path-to-hash manifest (subject to terms), grouping source and confidence, split IDs/seeds, overlap counts, label rules, inclusion/exclusion counts, and the exact benchmark task/metrics. Keep training, model selection, and final test partitions fixed before evaluating.

## Access notes and source links

Checked 2026-10-06. The official USU record page and both Mendeley record pages were readable. The official SDNET2018 file endpoints returned 403 through the research browser, so zip/readme contents were not verified. Dataset sizes and counts above are reported metadata, not an independent archive recount. No third-party mapping was accepted as authoritative without an underlying source manifest.

- [SDNET2018 official USU record, files, checksum, CC BY 4.0](https://digitalcommons.usu.edu/all_datasets/48/)
- [SDNET2018 data paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC6247444/)
- [CCIC Mendeley v1](https://data.mendeley.com/datasets/5y9wdsg2zt/1), [CCIC v2](https://data.mendeley.com/datasets/5y9wdsg2zt/2)
- [BCD original paper](https://doi.org/10.3390/app9142867), [author dataset repository](https://github.com/tjdxxhy/crack-detection)
- [BCL abstract](https://trid.trb.org/View/1875180)
- [PAGG-Net Zenodo record](https://zenodo.org/records/18010179)
- [Multi-temporal Crack Segmentation Zenodo record](https://zenodo.org/records/15187675)
- [OpenCrack dataset roster](https://github.com/fadeevla/OpenCrack)

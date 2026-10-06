# Search scope, screened counts, and research position

**Tags:** `systematic-search` `scoping-review` `model-count` `CNN-Transformer` `MobileViT` `research-gap` `novelty` `2026-10-06`

## Direct answers

### Is MobileViT-XS itself a CNN–Transformer hybrid?

Yes. MobileViT combines convolutional local processing with Transformer-based global processing inside repeated MobileViT blocks. Our baseline notebook imports the ImageNet-pretrained `mobilevit_xs.cvnets_in1k` implementation from `timm`, replaces its 1,000-class head with one crack/no-crack output, warms up that head, then fine-tunes the full model. We wrote the task-specific training workflow; we did not invent or reimplement MobileViT. See [MobileViT-XS baseline vs CrackFusion-Tiny](mobilevit_baseline_and_crackfusion_comparison.md).

### How is CrackFusion-Tiny different?

Both are hybrids, but their feature paths are arranged differently:

- **MobileViT-XS:** one staged feature stream repeatedly passes through convolutional processing and MobileViT blocks that unfold tokens, apply Transformer layers, fold features back to maps, and fuse them.
- **CrackFusion-Tiny:** a shared convolutional stem splits into a local CNN path and a Transformer path. The resulting maps are concatenated and fused once with a 1×1 convolution before the binary head.

The important difference is this particular layout and evaluation, not the general idea of combining convolution and attention. The MobileViT baseline uses ImageNet pretrained weights. The controlled CNN-only, Transformer-only, serial-hybrid, and CrackFusion comparisons in the project protocol are intended to isolate architecture effects under matched conditions.

### How many crack CNN–Transformer papers/models did this search find?

There is no authoritative field-wide total: the result changes depending on whether “hybrid” requires a distinct CNN feature path, whether a convolutional token embedding is enough, and whether classification, object detection, or pixel segmentation is included. **These are paper counts in a screened corpus, not counts of unique parameterized network variants.**

| Task | Screened count | Inclusion rule and interpretation |
|---|---:|---|
| Image-level crack / road-damage classification | **5 peer-reviewed candidates**, of which 4 are crack-specific and 1 is broader road damage including cracks | The classifier uses a learned convolutional feature-processing stage plus Transformer processing. This includes serial/staged hybrids, not only parallel branches. |
| Image-level crack classification preprint | **1** | EfficientCrackFusion is an explicit dual-backbone CNN–ViT classifier, currently identified as a Research Square preprint. Its stated parameter count conflicts with its ViT-Base description, so treat it cautiously. |
| Crack-specific localization / semantic-segmentation papers | **At least 22 published papers** in the 2023–2026 targeted screen | Distinct CNN and Transformer feature-processing components are explicitly integrated in a crack-specific pixel-mask network. Two adjacent candidates (SwinCrack and MaskerTransformer) are listed but excluded under this rule. |

The category counts are intentionally separate. A segmentation model that marks crack pixels is not a direct image-classification baseline. Across these screened categories, the search found **at least 27 peer-reviewed/publisher-listed papers plus one preprint**, but that combined number is not an exhaustive literature count and should not be described as 28 unique architectures. A paper may propose several variants; a later systematic database search may add papers or change borderline classifications.

## Closest prior work to our design

| Prior work | Closest overlap | Key difference from CrackFusion-Tiny |
|---|---|---|
| [CCTNet (2024)](https://doi.org/10.3390/s24134257) | Peer-reviewed concrete crack image classifier; includes SDNET2018 and convolution plus Transformer attention | Serial convolution-to-token/Transformer pipeline, rather than separate parallel local and global branches |
| [Shi and Luo (2025)](https://doi.org/10.1016/j.conbuildmat.2025.140793) | Peer-reviewed four-class intact/minor/moderate/severe concrete-crack classification; includes KAN-Hybrid and KAN-MobileViT variants | Different class target and model variants; the accessible abstract does not settle the exact KAN-Hybrid branch layout |
| [EfficientCrackFusion (2026 preprint)](https://doi.org/10.21203/rs.3.rs-8935135/v1) | Most explicit parallel CNN and Transformer binary crack classifier found | Describes independent EfficientNet-B0 and ViT-Base backbones with cross-attention; much larger claimed size; preprint's 12.8M total conflicts with its 86.6M ViT-Base table entry |
| [DefNet (2024)](https://doi.org/10.1016/j.conbuildmat.2024.138206), [DTrC-Net (2023)](https://doi.org/10.1016/j.autcon.2023.104894), and other dual-encoder segmenters | Separate CNN/local and Transformer/global feature paths with fusion | Pixel-mask task, larger encoders, multi-scale skips/decoders, and segmentation labels/metrics |
| [EfficientCrackNet (WACV 2025)](https://openaccess.thecvf.com/content/WACV2025/html/Zim_EfficientCrackNet_A_Lightweight_Model_for_Crack_Segmentation_WACV_2025_paper.html) | Reported 0.26M parameters, close to CrackFusion-Tiny's 0.284M; uses depthwise CNN blocks and MobileViT | Predicts pixel masks on Crack500/DeepCrack/GAPs384; task and architecture differ. It means parameter count alone cannot carry our novelty claim. |
| [Şermet and Pacal (2024)](https://dergipark.org.tr/en/pub/dumf/article/1450640) | Evaluates MobileViT XS/S/XXS and MobileViTv2 on SDNET2018 | Uses these as alternative backbones; it is not a newly fused, dual-branch CNN–Transformer proposal. Its split does not establish source-photo grouping. |

The detailed paper records, task distinctions, reported splits, and caveats are in [classification hybrids](crack_classification_hybrids.md) and [detection/segmentation hybrids](detection_segmentation_hybrids.md).

## What this implies for our paper

1. Do not claim we are the first to combine a CNN and Transformer for crack analysis, the first to use local/global fusion, or the first tiny hybrid crack model.
2. A plausible contribution is a **very compact image-level classifier with a shared stem, parallel local/global branches, and one fusion point**, tested against appropriate alternatives on SDNET2018.
3. Support that contribution with parent-photo-separated results, leave-one-surface-out tests, fair baselines, branch/fusion ablations, multiple seeds, and measured latency/memory. The project’s protocol lists these aims, but its current development split may contain parent-photo leakage and is not final evidence.
4. Keep the pretrained MobileViT-XS result as a practical transfer-learning reference. Use same-split, matched-initialization models to make the cleaner claim about whether a parallel local/global fusion helps.
5. The current parameter count is not enough to establish efficiency or scientific novelty. EfficientCrackNet is already reported at a comparable scale, although on segmentation.

The novelty should be framed as a **controlled study of a compact classifier and its generalization/efficiency trade-offs**, if the experiments support it—not as a new CNN–Transformer family.

## Search method and limits

### Search coverage

Search was conducted on **6 October 2026**. Targeted searches used combinations of:

- `concrete crack classification CNN Transformer`, `crack image classification CNN ViT`, `crack severity classification hybrid`
- `crack detection dual branch CNN Transformer`, `crack CNN Transformer local global fusion`
- `crack segmentation dual encoder`, `parallel CNN Transformer pavement crack`, `concrete bridge crack Transformer fusion`
- `MobileViT crack classification`, `MobileViT SDNET2018`, `EfficientCrackNet`
- dataset/evaluation searches for `SDNET2018 source image split`, `cross-surface crack classification`, and recent 2025–2026 crack datasets

Publisher and primary-source pages were preferred where available: IEEE/CVF, OpenReview, Springer Nature, Elsevier, ASCE, MDPI, Frontiers, Wiley/IET, institutional repositories, arXiv, and official dataset records. Publisher search results and citations inside located papers were used to find additional candidates. The older project Zotero snapshot and [existing literature synthesis](evidence/scope_existing_literature_synthesis.md) add foundational CNN/Transformer architecture references, reviews, and crack datasets.

### Inclusion and exclusion

- Count crack-specific image-level classifiers separately from crack-specific pixel-mask/localization papers.
- For the classification count, require image-/patch-level crack or road-damage labels and substantive learned convolutional feature processing plus Transformer processing in the prediction model. A convolution used only as a patch embed or positional encoding is a boundary case and is not counted in the strict screen.
- For the 22-paper segmentation set, require a crack-specific pixel-mask model with separately identifiable convolutional and Transformer feature-processing components that are explicitly integrated. Parallel and staged architectures are included; pure CNN, pure Transformer, convolution-only attention models, and object-detector pipelines are excluded from that core count.
- Count a paper once, even when it proposes multiple model variants or reports results on several datasets. Label preprints and ambiguous descriptions. Keep “adjacent” examples available for context without folding them into the narrow count.

### Limits

This is a **thorough targeted scoping review, not a PRISMA systematic review or citation census**. Search engines and databases index papers unevenly; terminology varies; some 2026 articles are new; non-English literature and inaccessible papers may be missed; and model methods are sometimes ambiguous or do not release code. Therefore, “22” and “5 + 1” describe this screened corpus only. A definitive total would require searching named scholarly databases with reproducible queries, exporting/deduplicating all records, and applying a documented paper-by-paper screening process.

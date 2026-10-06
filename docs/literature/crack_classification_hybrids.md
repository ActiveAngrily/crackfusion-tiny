# CNN–Transformer hybrids for crack classification

**Tags:** `crack-classification` `image-level` `CNN-Transformer` `CNN-ViT` `hybrid-model` `concrete-cracks` `SDNET2018` `binary-classification` `severity-classification` `MobileViT` `CCTNet` `EfficientCrackFusion`

**Search terms:** `crack classification CNN Transformer`, `concrete crack classification transformer fusion`, `image-level crack severity classification CNN ViT`, `SDNET2018 CNN transformer`, `MobileViT crack severity`, `road crack classification CNN ViT`.

**Coverage date:** 6 October 2026. This is a targeted, source-screened review of image-level classification papers, not a systematic-review census. It covers publisher records and accessible full text from Springer Nature, Elsevier, MDPI, Frontiers, Wiley/IET, IEEE, PubMed Central, and Research Square. A paper is counted as a classification candidate when its output is an image or patch class; segmentation and detection papers are listed separately even when they use a similar hybrid encoder.

## Short answer: how many are there?

There is no reliable single count because authors use “hybrid” for different designs: a CNN feeding a Transformer, a Transformer with convolutional blocks, or independent CNN and Transformer paths whose features are fused. In the papers screened here, **five peer-reviewed image-level crack or road-damage classification candidates** meet the inclusion rule below, and one additional concrete-crack classifier is currently a preprint. Four peer-reviewed candidates are crack-specific; one classifies broader road damage including cracks. Some are close to a two-branch CNN–Transformer model; others are serial or staged hybrids.

This is a **minimum confirmed in this search, not an exhaustive count of the field**. The inclusion rule requires an image-level crack/road-damage classifier with a learned convolutional feature-processing stage and Transformer processing in the prediction network. A convolution used only for patch embedding or positional encoding does not qualify by itself. If “hybrid” is further restricted to two independently encoded branches fused before classification, the count is smaller. Hybrid architectures are more numerous in pixel-level crack segmentation, which is a different task.

The closest published concrete-crack classification precedents are **CCTNet (2024)** and the **four-class severity study by Shi and Luo (2025)**. The clearest directly parallel dual-backbone classification design found is **EfficientCrackFusion**, but it is a 2026 preprint. The listed studies establish that combining local convolutional cues and Transformer context is an existing research direction. They do not establish that CrackFusion-Tiny’s particular compact layout has been tested under our intended evaluation protocol.

| Paper | Year/status | Classification output | Hybrid arrangement | Match to CrackFusion-Tiny |
|---|---:|---|---|---|
| [CCTNet: Bridging Convolutional Neural Networks and Transformers for Efficient Crack Detection in Concrete Building Structures](https://doi.org/10.3390/s24134257) | 2024, peer reviewed | Building crack image class; evaluated on SDNET2018 | Convolutional feature extraction followed by Transformer attention | Close task/domain; serial feature flow, not parallel branches |
| [Deep Learning for Automated Detection and Classification of Crack Severity Level in Concrete Structures](https://doi.org/10.1016/j.conbuildmat.2025.140793) | 2025, peer reviewed | Intact/minor/moderate/severe | Reports KAN-Hybrid and KAN-MobileViT among 12 models | Strong severity precedent; exact “Hybrid” topology needs full-text confirmation |
| [Crack Detection in Structural Images Using a Hybrid Swin Transformer and Enhanced Features Representation Block](https://doi.org/10.3389/frai.2025.1655091) | 2025, peer reviewed | Crack/no-crack | Swin Transformer with a convolutional feature representation block | Binary concrete task; convolution is integrated, not an independent CNN branch |
| [Vision Transformers–Kolmogorov–Arnold Networks-Based Consumer-Driven Surface Cracks Classification Model](https://doi.org/10.1038/s41598-026-40359-z) | 2026, peer reviewed | Crack/no-crack across concrete/asphalt images | MobileNetV3 features passed to LeViT, then enhanced Linformer/gated fusion and KAN head | Relevant lightweight staged CNN–Transformer comparison |
| [Hybrid Vision Transformer and Convolutional Network for Automated Road Damage Detection](https://doi.org/10.1049/ipr2.70330) | 2026, peer reviewed | Three road-damage classes, including cracks | CNN and ViT/SPT/MHSA features used for image-level classification | Nearby road-damage task; method description mixes “dual branch” and sequential fusion language |
| [EfficientCrackFusion: An EfficientNet-ViT Hybrid with Cross-Attention Fusion for Concrete Crack Detection](https://doi.org/10.21203/rs.3.rs-8935135/v1) | 2026, preprint | Crack/no-crack | Separate EfficientNet-B0 and ViT-Base encoders with bidirectional cross-attention | Closest explicit dual-branch classifier; preprint, 12.8M parameters |

## Paper notes

### 1. CCTNet — concrete image classification and SDNET2018

Yadav et al. propose the Convolution and Composite Attention Transformer Network (CCTNet) for concrete building crack classification. Its described flow starts with 2D convolutional spatial features, flattens those features into tokens, then processes them with Transformer attention. The attention design combines channel attention, window self-attention, and cross-window interaction before a softmax class head. In other words, the CNN forms the Transformer’s input representation; the method does not preserve a separate CNN classifier branch alongside a separate Transformer branch until the end.

The evaluation includes Historical Building Crack2019, SDNET2018, and the authors’ DS3 dataset. The paper reports high crack-classification scores, including on SDNET2018, but its reported aggregate values are not fully consistent across result tables. The SDNET2018 dataset itself contains more than 56,000 256×256 tiles derived from 230 original photographs. The CCTNet article reports fold-based results, but the accessible methodology does not establish that tiles were grouped by their parent photograph. Its scores therefore should not be compared directly with a parent-photo-separated result. Sources: [CCTNet article](https://doi.org/10.3390/s24134257), [SDNET2018 dataset paper](https://doi.org/10.1016/j.dib.2018.11.015).

**Why it matters here:** CCTNet is a peer-reviewed, concrete-image classifier using convolution and Transformer operations and includes SDNET2018. It makes a general “CNN plus Transformer for concrete crack classification” novelty claim untenable. Its serial conv-to-attention design differs from CrackFusion-Tiny’s shared stem followed by separate local and global branches with one concat-plus-1×1 fusion.

### 2. Shi and Luo — four-class concrete crack severity

Shi and Luo compare 12 models for four image labels: intact, minor, moderate, and severe. Their proposed variants replace the usual multilayer perceptron classifier with a Kolmogorov–Arnold Network (KAN) in ViT, Hybrid, and MobileViT models. They report an 8,000-image severity dataset assembled from CCIC and SDNET2018 sources and identify KAN-MobileViT as the strongest overall model in their experiments. The paper is a useful precedent for severity as an image-classification task. [Publisher article](https://doi.org/10.1016/j.conbuildmat.2025.140793)

The public abstract confirms the KAN-Hybrid and KAN-MobileViT model families and the four labels, but it does not give enough architectural detail to safely map the “Hybrid” model to a specific branch topology. The severity set also reuses source datasets, including SDNET2018. If a study trains on SDNET2018, this relabeled set should not automatically be treated as an independent external test set. The abstract describes severity classes but does not by itself establish physical crack-width thresholds or structural-risk labels; those definitions need checking in the full paper before citing it as calibrated severity measurement.

**Why it matters here:** This is a directly relevant published severity-classification precedent and a MobileViT-related comparison. It shows that “severity classification” is already being attempted; it does not make severity the right scope for our current SDNET2018 binary study.

### 3. Swin Transformer plus convolutional feature block — binary concrete classification

Reis et al. present a hybrid Swin Transformer with an Enhanced Features Representation Block (EFRB) and population-based feature selection. The article describes crack/no-crack classification on a 40,000-image set derived from 458 high-resolution concrete images and an 80:20 split. The EFRB uses depthwise and pointwise convolutions to refine features around a Swin Transformer; this is a convolution-augmented Transformer, rather than two full encoders running independently. [Frontiers article](https://doi.org/10.3389/frai.2025.1655091)

The article reports accuracy and IoU together for a classification-oriented task, and its available description does not specify whether the 40,000 crops were split by source photograph. Treat its reported values as the authors’ results, not a directly comparable benchmark for our planned source-separated evaluation.

**Why it matters here:** It is another peer-reviewed concrete binary classifier that combines convolution and Transformer operations. It reinforces the need to describe our contribution as a particular compact layout and evaluation, rather than as the first hybrid crack classifier.

### 4. MobileNetV3–LeViT–Linformer classifier

Wahab Sait et al. (2026) describe a staged classification pipeline: MobileNetV3 extracts convolutional features, those features are resized into a grid and passed to LeViT, and an enhanced Linformer plus gated fusion and a KAN classification head extend the representation. Their datasets include a 40,000-image positive/negative concrete set generated from 458 source photographs, an asphalt set, and a mixed Concrete Crack Conglomerate Dataset. They report a 70/15/15 train/validation/test division and use the mixed dataset for generalization evaluation. [Scientific Reports article](https://doi.org/10.1038/s41598-026-40359-z)

This is a useful staged lightweight CNN–Transformer comparison, but it is not a MobileViT model: LeViT and MobileViT are distinct architectures. MobileNetV3–LeViT passes one stage’s feature stream into the next and adds further attention/fusion components. MobileViT-XS uses repeated integrated MobileViT blocks. CrackFusion-Tiny instead has a shared convolutional stem, then a local CNN path and a Transformer path, followed by one explicit feature-map fusion. The project-specific account of MobileViT-XS is in [the baseline comparison note](mobilevit_baseline_and_crackfusion_comparison.md).

### 5. CNN–ViT road-damage image classifier

Kausar et al. (2026) classify road images into crack, pothole, and asphalt-deformation categories. The dataset contains 1,600 original Bangladesh road images; augmentation increases the training examples, while validation and test data are described as unaugmented. The method uses a CNN backbone with shifted patch tokenization and multi-head self-attention before an image-classification head, and evaluates transfer to RDD2020 and patches from CRACK500. The paper reports a 99.1% accuracy for its ResNet50–ViT model on its primary data. [IET/Wiley article](https://doi.org/10.1049/ipr2.70330)

This is a neighboring infrastructure classification task, not a concrete-only binary benchmark. Its text calls the architecture a dual-branch CNN–ViT model, while its feature equation also describes a CNN → SPT → MHSA sequence. That ambiguity makes it unwise to claim an exact layout match without examining the model figure and implementation. Its value for our review is evidence that fused local/global classification is now appearing in broader road-damage work.

### 6. EfficientCrackFusion — closest explicit parallel classifier, currently a preprint

Shah and Mahajan’s March 2026 Research Square preprint uses a dual-branch EfficientNet-B0 CNN and ViT-Base, each processing the same image. A bidirectional Cross-Attention Fusion Gate exchanges local and global features; a squeeze-and-excitation block and MLP head produce crack/no-crack output. The paper reports 40,000 images, a 70/10/20 group-aware split based on perceptual-hash similarity clusters, 12.8 million parameters, and 99.11% test accuracy. [Research Square preprint](https://doi.org/10.21203/rs.3.rs-8935135/v1)

This is the closest architectural comparison in the screened image-classification set because it explicitly keeps CNN and Transformer branches and fuses them before classification. It differs from CrackFusion-Tiny in fusion: it describes independent EfficientNet-B0 and ViT-Base backbones with bidirectional cross-attention; CrackFusion-Tiny is approximately 0.284 million parameters and uses a shared stem, parallel local/global paths, concatenation, and a 1×1 projection. **Do not rely on its stated 12.8M parameter count yet:** the same preprint identifies ViT-Base as 86.6M parameters in its comparison table, without explaining how the proposed network could then total 12.8M. The code or a later corrected version would be needed to resolve this internal inconsistency. Its reported scores, parameter count, and data-splitting claims should be treated as unreviewed claims until independently checked and/or a peer-reviewed version is located.

## Near-matches that should not be counted as image-level hybrid classifiers

Several influential and newer crack hybrids solve **pixel-level segmentation**, where every pixel receives a crack/background label. They are relevant when discussing local/global feature fusion, but their output and evaluation are different from our image-level crack/no-crack decision.

- [CrackViT (2023)](https://doi.org/10.1007/s00521-023-08277-7) uses a hybrid CNN–Transformer encoder for pixel-level crack extraction.
- [DTrC-Net (2023)](https://doi.org/10.1016/j.autcon.2023.104894) uses parallel CNN and Transformer encoders and fused decoder features for segmentation.
- [DMF-Net (published in IEEE T-ITS in 2024)](https://doi.org/10.1109/TITS.2023.3331769) uses dual CNN/Transformer encoders with interactive attention for pavement-crack segmentation.
- [CCDFormer (2025)](https://doi.org/10.1016/j.patcog.2024.111251) uses dual CNN and Transformer backbones with progressive feature fusion for segmentation.

These papers are especially important for novelty framing: **parallel CNN–Transformer feature extraction and fusion already exist in crack segmentation**, even though that does not prove an identical compact image classifier has been published.

The [CSW-S concrete crack classifier (2024)](https://doi.org/10.1038/s41598-024-54835-x) is another boundary case. It classifies crack/no-crack images with a CSWin Transformer and uses convolutional token embedding and depthwise-convolution positional encoding, but the paper does not describe a distinct CNN feature extractor. It is excluded from the five-paper count under the rule above. Its data are 17,000 224×224 crops from larger concrete-pavement images, randomly divided 70/30. Under a broader “any convolution plus attention” definition, it could be added, which is one reason there is no canonical field-wide count.

## Relation to our MobileViT-XS baseline and CrackFusion-Tiny

MobileViT-XS is itself a CNN–Transformer hybrid. In our baseline, pretrained MobileViT-XS from `timm` is fine-tuned for crack/no-crack. Its staged MobileViT blocks repeatedly mix convolution, tokenized self-attention, folding back to feature maps, and convolutional fusion. It is therefore a stronger conceptual comparison than a pure CNN baseline, but its pretrained initialization means the comparison is not a clean architecture-only experiment. See [MobileViT-XS baseline and CrackFusion-Tiny](mobilevit_baseline_and_crackfusion_comparison.md) for the implementation details.

CrackFusion-Tiny’s working distinction is its **particular layout and size**: a shared convolutional stem, one local CNN branch, one Transformer branch over the reduced feature map, then a single concatenation and 1×1 convolution. In the screened classification papers, CCTNet is serial conv-to-Transformer, the 2026 MobileNetV3–LeViT system is staged, the Swin/EFRB system is a convolution-augmented Transformer, and EfficientCrackFusion is parallel but uses full independent backbones and cross-attention. This comparison supports saying our design is a compact alternative worth testing; it does not support claiming that the general CNN–Transformer idea or local/global fusion is new.

The paper’s defensible contribution will depend on evidence: use a source-photo-separated evaluation for SDNET2018, report cross-surface generalization, compare against MobileViT-XS and a CNN baseline under transparent training conditions, and include ablations that remove either branch or the fusion. The model’s parameter count alone is not evidence of a useful efficiency–accuracy trade-off; latency and memory should be measured using the same hardware and input procedure.

## Search limits and follow-up

This review used targeted searches for crack/concrete classification, severity classification, CNN–Transformer fusion, MobileViT, and SDNET2018. It screened titles/abstracts and available publisher or repository text. It was not a PRISMA search, did not enumerate every conference paper or non-English publication, and did not verify every model implementation against source code. “Five peer-reviewed candidates plus one preprint” is therefore the count in this screened set, not a claim about every paper ever published.

For a full bibliography, the next useful pass is citation chaining from CCTNet, Shi and Luo, and the 2026 classification papers, followed by checking conference proceedings and model code. The most important unresolved details are the exact KAN-Hybrid architecture, group-based splitting for SDNET-derived tiles in the peer-reviewed classifier papers, and whether Kausar et al.’s text/figure describe parallel or sequential fusion.

**Related notes:** [MobileViT-XS baseline and CrackFusion-Tiny](mobilevit_baseline_and_crackfusion_comparison.md) · [Detection and segmentation hybrids](detection_segmentation_hybrids.md) · [Datasets and evaluation](datasets_evaluation_and_gaps.md)

# Literature Review: Compact Conv-Transformer Crack Classification

**Completed:** 2026-08-30\
**Scope:** all 22 top-level records in the Zotero group `major project` (library ID 2; group ID 6634536)\
This review provides the evidence base for the accompanying methodology.

## 1. Reading and evidence protocol

The editable Zotero target was re-checked before work began. The group contained 22 top-level records, all relevant to the project: two reviews, four foundations, ten vision/hybrid architecture papers, and six crack/dataset papers. Full text was read for all 22 records. The initially unavailable **MultiScaleCrackNet** article was supplied by the user and incorporated into this synthesis on 2026-08-30. No Zotero records or database files were modified.

Reported results below are the papers' own results, not independently reproduced values. Comparisons across papers are not direct rankings because datasets, resolutions, splits, pretraining, augmentations, compute, and metrics differ. In particular, random splitting of crops from the same source photograph can substantially inflate crack-classification performance.

## 2. Executive synthesis

### 2.1 What the literature establishes

1. **Convolution remains the cheapest reliable source of local bias.** ResNet, the early road-crack CNN, MultiScaleCrackNet, MobileViT, CMT, CvT, FastViT, and EfficientViT all exploit locality, translation structure, downsampling, or depthwise convolution. This is especially suitable for thin edges and texture discontinuities.
2. **Attention is most useful after spatial reduction.** Raw-pixel global attention is unnecessarily expensive for this project. CvT, Swin, CMT, MobileViT, CoAtNet, and EfficientViT reduce token count, restrict attention, or postpone attention to later stages.
3. **The most informative hybrids retain identifiable local and global paths.** Conformer, Mobile-Former, and CTRL-F make the interaction explicit. MobileViT offers the most practical small-model template; Conformer and CTRL-F offer clearer scientific fusion experiments but at higher implementation cost.
4. **Small-data success depends at least as much on training and evaluation as architecture.** DeiT demonstrates the effect of augmentation, regularisation, and distillation. The crack papers show very high in-domain scores, but often use crop-level or insufficiently documented splits. The two reviews and Omni-Crack30k make cross-domain validation, duplicate control, and reporting quality central research gaps.
5. **A defensible student contribution need not claim a new family of networks.** A small, parameter-matched experiment that isolates local features, global attention, and their fusion—under source-separated and cross-surface evaluation—fills a clearer gap than another large bespoke backbone.

### 2.2 Design implications

| Decision | Evidence-led choice for this project |
|---|---|
| Local extractor | Small residual/depthwise CNN stem; preserve thin-crack detail before aggressive downsampling. |
| Token source | Tokens formed from a CNN feature map, not raw image patches. This follows ViT's hybrid option and the efficient hybrids. |
| Attention | One or two small encoder blocks at a reduced spatial scale; standard attention is adequate at this token count. |
| Fusion | One explicit, inspectable fusion point: concatenate aligned local/global maps followed by a 1×1 convolution, optionally with one learned gate. |
| Training | ImageNet transfer where compatible; otherwise a DeiT-inspired but moderate augmentation recipe. Avoid a 300–1,000 epoch schedule unless an ablation justifies it. |
| Primary data | SDNET2018, with groups based on the 230 original source images rather than random crops. |
| Generalisation | Leave-one-surface-out tests across deck, wall, and pavement; optionally one genuinely external classification dataset. |
| Baselines | Parameter-matched CNN-only and Transformer-only models plus the fused hybrid. A standard pretrained ResNet-18 is a useful external baseline. |
| Metrics | Accuracy, balanced accuracy, precision, recall, F1, ROC-AUC, confusion matrix, parameters, MACs/FLOPs, and measured latency. Report mean and standard deviation across seeds. |
| Interpretation | Grad-CAM on the local branch and attention rollout/token maps on the global branch; test whether both focus on the crack rather than shadows or joints. |

## 3. Paper-by-paper extraction

### 3.1 Crack classification, datasets, and domain evidence

#### 1. SDNET2018: An Annotated Image Dataset for Non-Contact Concrete Crack Detection Using Deep Convolutional Neural Networks (`UBGE2XUB`)

**Source:** [Dorafshan et al., 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6247444/)

- **Architecture:** AlexNet transfer-learning benchmark; five convolutional layers followed by fully connected classification layers.
- **Convolution/attention interaction:** convolution only; no attention. It is a dataset/reference baseline rather than a hybrid.
- **Input representation:** 56,092 RGB crops of 256×256 pixels derived from 230 high-resolution photographs. The images retain difficult nuisances such as shadows, roughness, debris, holes, and surface markings.
- **Dataset and task:** binary crack/no-crack classification for bridge decks, walls, and pavements. Counts are 13,620 deck crops (2,025 positive), 18,138 wall crops (3,851 positive), and 24,334 pavement crops (2,608 positive), for 8,484 crack and 47,608 non-crack crops overall. Crack widths span approximately 0.06–25 mm.
- **Training setup:** AlexNet was evaluated through fine-tuning and transfer learning. Transfer learning converged in about 10 epochs versus 32 for full fine-tuning in the reported setup.
- **Metrics/results:** transfer-learning accuracies were 91.92% for decks, 89.31% for walls, and 95.52% for pavements; corresponding fine-tuning results were 90.45%, 87.54%, and 94.86%.
- **Limitations:** severe class imbalance; crops inherit correlations from only 230 originals; patch-level random splitting could leak scene, camera, and texture information; the three surface domains differ substantially. Accuracy alone hides minority-class performance.
- **Code/data availability:** dataset is openly available; the paper does not provide a maintained end-to-end model repository.
- **Practical lesson:** this should be the primary dataset, but all crops from one source photograph must remain in the same partition. Surface type should be retained as a domain label, enabling leave-one-surface-out evaluation. Class-balanced sampling or loss weighting and balanced metrics are essential.

#### 2. Road Crack Detection Using Deep Convolutional Neural Network (`9RL32V4L`)

**Source:** [Zhang et al., 2016 author manuscript](https://yiminzhang.com/pdf0/icip16.pdf)

- **Architecture:** a compact CNN with convolution, max pooling, fully connected layers, dropout, ReLU, and softmax.
- **Convolution/attention interaction:** convolution only; the model learns local crack texture without a global-context mechanism.
- **Input representation:** 99×99 RGB patches sampled from more than 500 smartphone pavement images of 3264×2448 pixels. A patch is positive when its centre is within five pixels of a labelled crack. Rotation is used both for training and test-time averaging.
- **Dataset and task:** balanced binary road-crack patch classification: 640,000 training, 160,000 validation, and 200,000 test patches.
- **Training setup:** Caffe; SGD with batch 48, momentum 0.9, weight decay 0.0005, dropout 0.5, fewer than 20 epochs, and five-fold cross-validation. The operating threshold (0.64) was selected on validation data, and five rotated predictions were averaged at test time.
- **Metrics/results:** precision 0.8696, recall 0.9251, and F1 0.8965, outperforming the reported SVM (F1 0.7359) and boosting (F1 0.7472) baselines.
- **Limitations:** pavement is not the full concrete-building domain; dense patch classification is computationally inefficient; the split relationship between source photos and sampled patches is not strong evidence of cross-scene generalisation; the model is now a weak architectural baseline.
- **Code/data availability:** no official code repository was identified; the author manuscript is open.
- **Practical lesson:** high recall matters for safety-oriented crack screening, but patch counts are not independent sample counts. Use source-level partitions and image-level inference rather than reproducing dense sliding-window classification.

#### 3. Bridging CNNs and Transformers in the Detection of Concrete Cracks: CCTNet (`B9X3LZ38`)

**Source:** [Yadav et al., 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11243917/)

- **Architecture:** CCTNet combines convolutional spatial feature extraction with a composite-attention Transformer. Features are tokenised and processed by window multi-head self-attention, convolutional channel attention, and overlapping cross-attention between windows, followed by classification.
- **Convolution/attention interaction:** convolution supplies local/spatial and channel-biased features; window attention models longer-range structure; overlapping cross-attention reconnects otherwise isolated windows.
- **Input representation:** RGB images resized to 300×300; reported local patch size is 11×11.
- **Dataset and task:** binary classification on Historical Building Crack2019 (757 crack, 3,139 non-crack) and the SDNET2018 wall subset (3,851 crack, 14,287 non-crack); six-class surface-condition classification on DS3 (2,115 originals, augmented to 2,000 images per class).
- **Training setup:** Adam, batch 64, learning rate 10⁻⁴, binary cross-entropy for binary tasks, 200 epochs, rotation/flipping augmentation, and five-fold cross-validation for the two crack datasets. DS3 uses an 80/20 random split.
- **Metrics/results:** reported accuracy/F1 are 98.59%/99.12% on Historical Building Crack2019, 99.24%/99.31% on SDNET walls, and 99.37%/99.35% on DS3. A separate unseen bridge experiment reports 97.79% accuracy and 95.49% F1, a more meaningful indicator of generalisation.
- **Limitations:** very high in-domain results depend on split construction and augmentation; binary experiments use imbalanced data; the paper acknowledges limited generalisation to unseen conditions/materials, labelling demand, and lower-end hardware constraints. The architecture is too elaborate for the smallest student project.
- **Code/data availability:** no official public code repository was found in the paper; datasets are referenced.
- **Practical lesson:** overlapping/local attention can preserve thin-crack continuity, but the key lesson is to include a separate unseen-domain test. A simpler single fusion point is easier to ablate and defend.

#### 4. An Improved Transformer-Based Concrete Crack Classification Method (`WII7ZDKS`)

**Source:** [Ye et al., 2024](https://www.nature.com/articles/s41598-024-54835-x.pdf)

- **Architecture:** CSW-S uses an overlapping 7×7 stride-4 convolutional token embedding, four Cross-Shaped Window Transformer stages, horizontal/vertical stripe attention, locally enhanced positional encoding through depthwise convolution, and multi-level residual skip fusion.
- **Convolution/attention interaction:** convolution creates overlapping local tokens and injects local positional information; cross-shaped attention covers long horizontal and vertical crack structures; skip fusion reuses shallow detail.
- **Input representation:** 224×224 RGB crops produced from 1,000 pavement photographs of 4000×4000 pixels.
- **Dataset and task:** 17,000 binary crack/no-crack crops, split 11,900/5,100 (7:3). Crack types include longitudinal, transverse, and fatigue cracks.
- **Training setup:** PyTorch on one Quadro RTX A5000; training from scratch with SGD, batch 2, weight decay 0.0005, dropout 0.5. The text reports learning-rate experiments and a best base rate of 10⁻⁴, but contains inconsistent schedule wording. It reports 230 training iterations/epochs and best validation performance around epoch 109.
- **Metrics/results:** accuracy 96.92%, precision 98.65%, recall 95.13%, specificity 98.70%, F1 96.85%, and mIoU 94.03%. Reported accuracy baselines include ViT at 78.15%, Swin-T at 96.15%, and CSWin at 95.66%.
- **Limitations:** images are described as free from complex environmental obstacles; the dataset is available only on request; crops may share source-image characteristics across splits; tiny batch training and inconsistent schedule descriptions complicate reproduction. The printed formulas for recall and specificity contain denominator errors, so the implementation and reported labels should be checked rather than copied.
- **Code/data availability:** no code repository was provided; data are available from the authors on request.
- **Practical lesson:** overlapping convolutional tokens and directional attention suit elongated cracks, but recreating the full CSWin design is unnecessary. Preserve overlap/locality and test on nuisance-rich SDNET images instead.

#### 5. MultiScaleCrackNet (`KU57S9P4`)

**Source:** [Russel and Selvaraj, 2024 publisher record](https://doi.org/10.1016/j.eswa.2024.123658)

- **Evidence status:** the complete 11-page published article was supplied by the user and read in full.
- **Architecture:** a 71-layer, approximately 1.3M-parameter hierarchical CNN with three parallel streams. A 128×128 input is processed at full, half, and quarter spatial scales. The deepest stream uses three convolution groups, the middle stream two, and the shallow stream one; all reach 16×16 before concatenation into a 136-channel feature map. Three further 3×3 convolution/pooling groups (128, 256, and 256 channels) precede the fully connected softmax classifier.
- **Convolution/attention interaction:** convolution only; there is no Transformer or attention branch. The important hybridisation is between fixed image-processing filters and learned CNN filters, not between convolution and attention.
- **Input representation:** 128×128 RGB images. In each stream's first convolution, one predefined low-pass filter and seven predefined high-pass/edge filters capture low- and high-frequency structure. The paper evaluates customised-filter-only, learnable-filter-only, and combined customised-plus-learnable variants.
- **Dataset and task:** binary crack/no-crack classification on Concrete Crack Images for Classification (40,000 images; 20,000 per class), Asphalt Crack Dataset (400 images), and separate SDNET2018 deck, pavement, and wall subsets. It also evaluates the complete SDNET collection as a six-class task representing crack/non-crack across the three surface types.
- **Training setup:** backpropagation with SGD, cross-entropy loss, initial learning rate 0.001, momentum 0.90, mini-batch 28, and 30 epochs. The Concrete Crack Images experiment uses a 75/25 train/test split and explicitly applies no augmentation. Separate split details for Asphalt and SDNET, source-image grouping, weight decay, scheduling, and validation/model-selection procedures are not reported clearly.
- **Metrics/results:** the combined fixed-plus-learned model reports 99.6% accuracy, 99.3% precision, 99.9% recall, and 99.6% F1 on Concrete Crack Images; and 99.0% accuracy, 100% precision, 98.0% recall, and 99.0% F1 on the small Asphalt dataset. Results are substantially weaker on imbalanced SDNET binary subsets: deck 88.9% accuracy/33.8% recall/47.5% F1; pavement 92.9%/54.4%/62.2%; wall 85.5%/58.4%/63.0%. On the six-class SDNET task, the combined model reports 90.7% accuracy, 86.5% precision, 78.2% recall, 81.3% F1, MCC 79.9%, and kappa 66.6%.
- **Comparative findings:** the proposed model is compact, but it does not dominate pretrained CNNs on the three binary SDNET subsets. Darknet reaches 92.9% accuracy and 72.4% F1 on decks; DenseNet/EfficientNet reach 96.2% accuracy and 81.2% F1 on pavements; EfficientNet reaches 93.1% accuracy and 82.0% F1 on walls. The proposed combined model does lead the paper's six-class SDNET accuracy table despite using far fewer parameters than most pretrained comparators.
- **Interpretability:** the paper visualises early and deeper activation maps, showing progressively highlighted crack regions. It does not provide attribution validation, attention maps, or a quantitative localisation analysis.
- **Limitations:** the Asphalt set is extremely small; the 75/25 protocol is not source-separated; the paper itself warns that near-perfect results may reflect controlled data or memorisation. SDNET's low crack recall demonstrates that high accuracy can hide minority-class failure. No cross-dataset training/testing experiment is reported, and baseline fine-tuning fairness is insufficiently specified. The authors also identify limited real-world diversity and training/inference cost as constraints.
- **Code/data availability:** data are stated to be available on request; the two public datasets are cited, but no official code repository or split manifest is provided.
- **Practical lesson:** use MultiScaleCrackNet as a compact CNN-only baseline and as motivation for a fixed-edge-filter or three-scale ablation. Its SDNET results reinforce the need for balanced metrics, source-separated partitions, and cross-surface evaluation; the near-perfect balanced-dataset scores should not be used as the primary success criterion.

#### 6. Omni-Crack30k (`RBFNPZW6`)

**Source:** [Benz and Rodehorst, 2024](https://openaccess.thecvf.com/content/CVPR2024W/VAND/papers/Benz_OmniCrack30k_A_Benchmark_for_Crack_Segmentation_and_the_Reasonable_Effectiveness_CVPRW_2024_paper.pdf)

- **Architecture:** this is primarily a benchmark paper. It evaluates crack-specific segmentation networks and general-purpose models including nnU-Net, DeepLabV3, BEiT/UPerNet, and Mask2Former.
- **Convolution/attention interaction:** comparison rather than a new hybrid; it shows that well-tuned general CNN and Transformer systems can rival or exceed specialised crack networks.
- **Input representation:** a curated union of 20 crack subsets with standardised segmentation masks; the nnU-Net reference uses 256×256 inputs.
- **Dataset and task:** pixel-level crack segmentation, not image classification. Omni-Crack30k contains 30,017 images: 22,158 train, 3,277 validation, and 4,582 test.
- **Training setup:** the nnU-Net reference uses cross-entropy plus Dice loss and a five-fold ensemble. Test results are retained by source subset to expose domain variation.
- **Metrics/results:** the main tolerance-aware measure is clIoU at four pixels. Average reported clIoU is 63.7% for nnU-Net, 52.9% for Mask2Former, 43.2% for BEiT/UPerNet, and 40.4% for DeepLabV3. In-the-wild subsets remain difficult.
- **Limitations:** segmentation labels and metrics cannot be directly compared with binary classification; combining public datasets does not eliminate domain bias; the strongest nnU-Net result uses an ensemble.
- **Code/data availability:** the consolidated dataset, evaluation material, and code are linked by the paper.
- **Practical lesson:** the authors found exact or near duplicate datasets and train/test leakage in existing collections. Duplicate removal, source-preserving splits, and per-domain results are more valuable to this project than using Omni-Crack30k as the primary data. It may provide an optional external challenge set only if classification labels are derived transparently.

### 3.2 Foundations

#### 7. Attention Is All You Need (`M9GHNUCF`)

**Source:** [Vaswani et al., 2017](https://papers.neurips.cc/paper/7181-attention-isall-you-need.pdf)

- **Architecture:** six-layer encoder and decoder stacks using multi-head self-attention, encoder-decoder attention, position-wise feed-forward networks, residual connections, layer normalisation, and sinusoidal position encodings.
- **Convolution/attention interaction:** none; the central contribution replaces recurrence and convolution with attention.
- **Input representation:** subword-token sequences with learned embeddings plus position encodings.
- **Dataset and task:** WMT 2014 English–German (about 4.5 million sentence pairs) and English–French (about 36 million) neural machine translation.
- **Training setup:** Adam with β₁=0.9, β₂=0.98, ε=10⁻⁹, 4,000 warm-up steps followed by inverse-square-root decay, dropout 0.1, and label smoothing 0.1. The base model trained for 100,000 steps and the big model for 300,000 on eight P100 GPUs.
- **Metrics/results:** BLEU 28.4 on English–German and 41.0 on English–French for the large model.
- **Limitations:** not a vision or crack study; standard self-attention scales quadratically with sequence length and lacks built-in two-dimensional/local visual bias.
- **Code/data availability:** the paper references the Tensor2Tensor implementation; machine-translation datasets are established public benchmarks.
- **Practical lesson:** use scaled dot-product attention, residual connections, normalisation, and positional information, but form only a short sequence from reduced CNN features.

#### 8. Deep Residual Learning for Image Recognition (`GH8EIH8C`)

**Source:** [He et al., 2016](https://openaccess.thecvf.com/content_cvpr_2016/papers/He_Deep_Residual_Learning_CVPR_2016_paper.pdf)

- **Architecture:** residual networks learn `F(x)+x`; ResNet-18/34 use basic blocks and ResNet-50/101/152 use 1×1–3×3–1×1 bottlenecks, with projection shortcuts when dimensions change.
- **Convolution/attention interaction:** convolution only. Residual connections later become equally important in Transformer blocks.
- **Input representation:** ImageNet RGB images using 224×224 crops, scale augmentation, horizontal flips, and colour augmentation.
- **Dataset and task:** ImageNet-1K image classification (about 1.28 million training and 50,000 validation images), with additional COCO detection/segmentation transfer experiments.
- **Training setup:** SGD, batch 256, initial learning rate 0.1 reduced on plateaus, momentum 0.9, weight decay 0.0001, batch normalisation, and up to 600,000 iterations; no dropout in the ImageNet residual networks.
- **Metrics/results:** ResNet-152 reports 19.38% single-crop top-1 error and 4.49% top-5 error; a six-model ensemble reports 3.57% top-5 error.
- **Limitations:** local receptive fields expand indirectly; a deep ResNet is more compute than needed for a binary student project; original multi-crop testing should not be compared with single-crop results without disclosure.
- **Code/data availability:** standard reference implementations are widely available; the paper itself is the architectural specification rather than a current maintained repository.
- **Practical lesson:** use residual blocks in the CNN baseline and local branch. ResNet-18 transfer learning is the strongest simple external baseline; a smaller custom stem should be used for parameter-matched ablations.

#### 9. An Image Is Worth 16×16 Words: Transformers for Image Recognition at Scale (`P62GMGTN`)

**Source:** [Dosovitskiy et al., 2021](https://arxiv.org/pdf/2010.11929)

- **Architecture:** fixed non-overlapping image patches are flattened and linearly projected, a class token and learned positions are added, and a pre-normalised Transformer encoder feeds an MLP classifier. The paper also evaluates a hybrid in which tokens are patches or individual positions from a CNN feature map.
- **Convolution/attention interaction:** the pure model has none; the hybrid option uses convolution before attention but does not maintain an explicit local branch at the output.
- **Input representation:** typically 16×16 or 32×32 raw-image patches; hybrid tokens can be 1×1 positions from a ResNet feature map.
- **Dataset and task:** pretraining on ImageNet-1K (1.3M images), ImageNet-21K (14M), and JFT-300M (303M), followed by transfer to ImageNet, CIFAR-10/100, Oxford Pets, Flowers-102, and VTAB-19.
- **Training setup:** Adam (β₁=0.9, β₂=0.999), batch 4,096, weight decay 0.1, linear warm-up/decay; downstream fine-tuning uses momentum SGD, batch 512, and often higher input resolution with interpolated position embeddings.
- **Metrics/results:** JFT-pretrained ViT-H/14 reports 88.55% ImageNet top-1, while ImageNet-21K-pretrained ViT-L/16 reports 85.30%. Larger ViTs underperform smaller ones when trained on ImageNet alone, demonstrating data dependence.
- **Limitations:** models are huge (86M–632M parameters); strongest results depend on inaccessible JFT-300M pretraining; weak visual inductive bias makes small-data training difficult; attention cost grows with token count.
- **Code/data availability:** [official Google Research implementation](https://github.com/google-research/vision_transformer); JFT is not public.
- **Practical lesson:** the CNN-feature-token hybrid is the relevant idea. A raw-patch ViT should be only a small matched baseline, not the proposed model.

#### 10. Training Data-Efficient Image Transformers and Distillation through Attention (`CXTFQ3YB`)

**Source:** [Touvron et al., 2021](https://proceedings.mlr.press/v139/touvron21a/touvron21a.pdf)

- **Architecture:** DeiT retains the ViT encoder and adds a distillation token whose final prediction learns from a CNN teacher; class-token and distillation-token outputs are averaged at inference.
- **Convolution/attention interaction:** no convolution inside the student; CNN inductive bias enters through teacher supervision and attention-mediated interaction between the class and distillation tokens.
- **Input representation:** 224×224 images as 16×16 patches, with a 384×384 fine-tuning stage for selected models.
- **Dataset and task:** ImageNet-1K classification without external pretraining data.
- **Training setup:** AdamW, batch 1,024, roughly 300 epochs (plus longer experiments), learning rate around 5×10⁻⁴ with scaling, weight decay 0.05, cosine schedule, RandAugment, random erasing, Mixup, CutMix, repeated augmentation, stochastic depth, and hard distillation from RegNetY-16GF.
- **Metrics/results:** DeiT-B reaches 81.8% top-1 at 224; distilled DeiT-B reaches 83.4% at 224 and 84.5% after 384 fine-tuning in the 300-epoch setting.
- **Limitations:** long, augmentation-heavy training and a large teacher are not minimal; distillation complicates attribution of gains; it does not explicitly preserve a local feature branch.
- **Code/data availability:** [official DeiT repository](https://github.com/facebookresearch/deit).
- **Practical lesson:** small-data Transformer comparisons require serious regularisation and augmentation. For fairness, use the same augmentation across matched models; treat distillation as an optional later experiment, not the core contribution.

### 3.3 Vision Transformers, hybrids, and efficient designs

#### 11. Swin Transformer (`GTCI5SK8`)

**Source:** [Liu et al., 2021](https://openaccess.thecvf.com/content/ICCV2021/papers/Liu_Swin_Transformer_Hierarchical_Vision_Transformer_Using_Shifted_Windows_ICCV_2021_paper.pdf)

- **Architecture:** a four-stage hierarchical Transformer with patch merging. Window self-attention alternates with shifted-window attention, enabling cross-window exchange while retaining linear complexity in image size; relative position bias encodes local geometry.
- **Convolution/attention interaction:** no explicit convolutional branch; windows and hierarchy introduce CNN-like locality and multiscale structure.
- **Input representation:** non-overlapping 4×4 patches followed by progressively merged tokens.
- **Dataset and task:** ImageNet-1K/22K classification, COCO object detection, and ADE20K semantic segmentation.
- **Training setup:** ImageNet-1K models are trained for 300 epochs with AdamW and modern augmentation; ImageNet-22K pretraining uses 90 epochs followed by ImageNet-1K fine-tuning.
- **Metrics/results:** Swin-T reports 81.3% ImageNet top-1 at 29M parameters/4.5G FLOPs; Swin-B reports 83.5%; ImageNet-22K-pretrained Swin-L reports 87.3%. Shifted windows improve accuracy over non-shifted local windows in the ablation.
- **Limitations:** hierarchy and shifted-window masking increase implementation complexity; there is no independently measurable CNN path; full-scale variants exceed the project's compute needs.
- **Code/data availability:** [official Microsoft repository](https://github.com/microsoft/Swin-Transformer).
- **Practical lesson:** local attention plus occasional cross-window exchange is efficient, but reduced CNN-feature tokens make standard attention simple enough for the proposed small model.

#### 12. CvT: Introducing Convolutions to Vision Transformers (`LQT8CXBK`)

**Source:** [Wu et al., 2021](https://openaccess.thecvf.com/content/ICCV2021/papers/Wu_CvT_Introducing_Convolutions_to_Vision_Transformers_ICCV_2021_paper.pdf)

- **Architecture:** three hierarchical stages with overlapping convolutional token embeddings and depthwise-separable convolutional projections for queries, keys, and values. Strided key/value projections reduce attention cost; a class token appears only in the final stage.
- **Convolution/attention interaction:** convolution supplies locality, translation structure, overlap, and downsampling directly inside tokenisation and attention projections; global attention follows at each stage.
- **Input representation:** overlapping convolutional feature tokens; explicit absolute positional embeddings are unnecessary.
- **Dataset and task:** ImageNet-1K/22K classification with downstream detection and segmentation transfer.
- **Training setup:** ImageNet-1K training uses AdamW, 300 epochs, batch 2,048, cosine scheduling, weight decay 0.05/0.1, and ViT-style augmentation; downstream fine-tuning settings vary by task.
- **Metrics/results:** CvT-13 reports 81.6% top-1 at 20M parameters/4.5G FLOPs; CvT-21 reports 82.5% at 32M/7.1G and 83.3% at 384 resolution. Ablations show gains from both convolutional embedding and convolutional projection.
- **Limitations:** multi-stage convolution inside every attention block is more machinery than needed here; reported large-model gains still use large-scale pretraining; it fuses implicitly rather than exposing branch contributions.
- **Code/data availability:** [official Microsoft CvT repository](https://github.com/microsoft/CvT).
- **Practical lesson:** overlapping convolutional tokenisation is a high-value, low-risk idea. It can be implemented by forming tokens from the local CNN feature map without reproducing all three CvT stages.

#### 13. Conformer: Local Features Coupling Global Representations (`GWUJX2DK`)

**Source:** [Peng et al., 2021](https://openaccess.thecvf.com/content/ICCV2021/papers/Peng_Conformer_Local_Features_Coupling_Global_Representations_for_Visual_Recognition_ICCV_2021_paper.pdf)

- **Architecture:** concurrent CNN and Transformer branches. Feature Coupling Units repeatedly align feature maps and patch tokens through pooling/interpolation and 1×1 projections; CNN and Transformer classifier outputs are combined.
- **Convolution/attention interaction:** explicitly bidirectional and multi-level: local features are injected into tokens and global representations are mapped back into CNN features.
- **Input representation:** a convolutional stem supplies the CNN path and patch embeddings for the Transformer path; resolutions are aligned at coupling units.
- **Dataset and task:** ImageNet-1K classification plus COCO detection and instance segmentation.
- **Training setup:** AdamW, 300 epochs, batch 1,024, learning rate 0.001, weight decay 0.05, cosine schedule, and DeiT-style Mixup, CutMix, random erasing, RandAugment, and stochastic depth.
- **Metrics/results:** Conformer-Ti reaches 81.3% top-1 at 23.5M parameters/5.2G FLOPs; Conformer-S reaches 83.4%; Conformer-B reaches 84.1%. Ablations favour the coupled dual structure over simple serial or ensemble alternatives.
- **Limitations:** repeated bidirectional coupling, alignment, and dual classifiers increase code, compute, and ablation burden. It is unsuitable for a minimum implementation even though it is the clearest conceptual reference.
- **Code/data availability:** [official Conformer repository](https://github.com/pengzhiliang/Conformer).
- **Practical lesson:** make local/global interaction explicit and compare branch-specific outputs, but use one fusion site rather than many coupling units.

#### 14. CoAtNet: Marrying Convolution and Attention for All Data Sizes (`2KCLWMMZ`)

**Source:** [Dai et al., 2021](https://proceedings.neurips.cc/paper_files/paper/2021/file/20568692db622456cc42a2e853ca21f8-Paper.pdf)

- **Architecture:** a serial five-stage family: early convolution/MBConv stages followed by later relative-attention Transformer stages. The analysis relates depthwise convolution to relative attention and orders stages to balance generalisation and capacity.
- **Convolution/attention interaction:** sequential rather than parallel; local convolution reduces resolution before global attention.
- **Input representation:** hierarchical feature maps; later spatial features are treated as attention tokens.
- **Dataset and task:** ImageNet-1K/21K and JFT-300M/3B image classification.
- **Training setup:** representative schedules use 300 epochs on ImageNet-1K, 90 on ImageNet-21K, or 14 on JFT at 224 resolution, followed by about 30 epochs of higher-resolution fine-tuning; strong augmentation and regularisation are used.
- **Metrics/results:** CoAtNet-0 reports 81.6% top-1 at 25M parameters/4.2G FLOPs; CoAtNet-2 reports 84.1%; larger models with massive pretraining reach 88.56% (ImageNet-21K) and 90.88% (JFT-3B).
- **Limitations:** strongest claims rely on resources far beyond a student project; sequential fusion cannot directly show what each branch contributes; scale dominates the headline results.
- **Code/data availability:** no official implementation was identified in the Zotero record; third-party implementations exist but are outside this extraction.
- **Practical lesson:** put convolution early and attention late. Do not reproduce the large scaling programme or cite its headline result as an attainable target.

#### 15. CMT: Convolutional Neural Networks Meet Vision Transformers (`AGUTHS2H`)

**Source:** [Guo et al., 2022](https://openaccess.thecvf.com/content/CVPR2022/papers/Guo_CMT_Convolutional_Neural_Networks_Meet_Vision_Transformers_CVPR_2022_paper.pdf)

- **Architecture:** a convolutional stem followed by four hierarchical stages. Each CMT block contains a depthwise-convolution Local Perception Unit, lightweight attention with spatially reduced keys/values, and an inverted-residual feed-forward network containing depthwise convolution.
- **Convolution/attention interaction:** local convolution occurs before attention and inside the feed-forward path; attention supplies longer-range dependencies at reduced cost.
- **Input representation:** hierarchical convolutional feature maps/tokens with progressive downsampling.
- **Dataset and task:** ImageNet-1K classification, COCO detection, and ADE20K segmentation.
- **Training setup:** AdamW, generally 300 epochs (longer for the tiny variant), eight V100 GPUs, and DeiT-style augmentation.
- **Metrics/results:** CMT-S reports 83.5% top-1 at 25.1M parameters/4.0G FLOPs; CMT-B 84.5%; CMT-L 84.8%. Its ablation progresses from a staged DeiT at 79.8% to 83.5% after adding the convolutional stem, local perception, convolutional feed-forward design, and projection choices.
- **Limitations:** convolution is intertwined with every block, making clean local-versus-global attribution difficult; four stages exceed the minimum viable model.
- **Code/data availability:** implementation is linked through [Huawei Noah's CV-Backbones repository](https://github.com/huawei-noah/CV-Backbones).
- **Practical lesson:** a depthwise local block plus spatially reduced attention is efficient. For this project, isolate those roles into separately ablatable branches.

#### 16. MobileViT (`UZT7VV56`)

**Source:** [Mehta and Rastegari, 2022](https://arxiv.org/pdf/2110.02178)

- **Architecture:** a MobileNet-style CNN feeds MobileViT blocks. Each block applies local convolution, projects channels, unfolds the feature map into structured patches, applies a Transformer across patches for each within-patch position, folds the result back, projects it, concatenates it with the input, and fuses with convolution.
- **Convolution/attention interaction:** explicit serial-and-fusion interaction: convolution captures local spatial patterns; attention links distant patches; concatenation and convolution restore local/global feature maps.
- **Input representation:** feature-map patches rather than flattened raw pixels, preserving within-patch spatial order.
- **Dataset and task:** ImageNet-1K classification with downstream object detection and segmentation.
- **Training setup:** trained from scratch for 300 epochs on eight GPUs, batch 1,024, AdamW, label smoothing 0.1, multi-scale sampling (roughly 160–320), warm-up then cosine learning rate, weight decay 0.01, random crop/flip, and EMA.
- **Metrics/results:** MobileViT-XS reports 74.8% top-1 at 2.3M parameters/0.7G FLOPs; MobileViT-S reports 78.4% at 5.6M/2.0G. Despite low FLOPs, measured mobile latency is higher than similarly sized MobileNetV2, showing that FLOPs are not latency.
- **Limitations:** unfold/fold operations and Transformer kernels can be slow on actual mobile devices; extensive scratch training is still expensive; the full network contains several blocks and tasks beyond project needs.
- **Code/data availability:** [official Apple ML-CVnets repository](https://github.com/apple/ml-cvnets).
- **Practical lesson:** this is the best starting blueprint. Use one or two simplified feature-token blocks and measure real latency rather than relying on parameter/FLOP counts.

#### 17. Mobile-Former (`F38CEX55`)

**Source:** [Chen et al., 2022](https://openaccess.thecvf.com/content/CVPR2022/papers/Chen_Mobile-Former_Bridging_MobileNet_and_Transformer_CVPR_2022_paper.pdf)

- **Architecture:** parallel MobileNet and small-token Transformer branches, usually with six learned global tokens. Lightweight cross-attention bridges transfer information both ways; global tokens also control dynamic ReLU in the mobile branch.
- **Convolution/attention interaction:** bidirectional cross-attention repeatedly connects dense local features with a tiny global-token set.
- **Input representation:** a spatial MobileNet feature map plus a fixed small bank of learned global tokens, rather than one token per image patch.
- **Dataset and task:** ImageNet-1K classification and downstream detection.
- **Training setup:** from-scratch AdamW training for about 450 epochs, batch 1,024, cosine decay, and Mixup, AutoAugment, and random erasing; exact rates/regularisation vary by model size.
- **Metrics/results:** the 294M-MAdd model reports 77.9% top-1 at 11.4M parameters; the 508M-MAdd model reports 79.3%. The Former and bridge produce a reported 2.6-point gain at about 12% additional compute in an ablation.
- **Limitations:** repeated cross-attention and dynamic activations add complexity; the classifier head holds a large fraction of parameters in small variants; training is long; actual device efficiency varies with image size.
- **Code/data availability:** [official Mobile-Former repository](https://github.com/aaboys/mobileformer).
- **Practical lesson:** a very small global-token set is attractive, but repeated bidirectional bridges are unnecessary. A single learned fusion gate captures the testable idea with much less code.

#### 18. FastViT (`4YLNLIG8`)

**Source:** [Vasu et al., 2023](https://openaccess.thecvf.com/content/ICCV2023/papers/Vasu_FastViT_A_Fast_Hybrid_Vision_Transformer_Using_Structural_Reparameterization_ICCV_2023_paper.pdf)

- **Architecture:** hierarchical convolutional stem and patch embeddings; RepMixer blocks and large-kernel convolutional feed-forward networks in early stages; self-attention in the final stage. Structural reparameterisation merges training-time branches into a single depthwise convolution for inference.
- **Convolution/attention interaction:** convolution handles high-resolution stages; attention is delayed until tokens are few; the model is serial rather than an explicit dual branch.
- **Input representation:** hierarchical feature maps, generally 224×224 images with 384 fine-tuning for selected variants.
- **Dataset and task:** ImageNet-1K classification plus downstream detection, segmentation, robustness, and 3D tasks.
- **Training setup:** AdamW, 300 epochs, batch 1,024, peak learning rate 0.001, weight decay 0.05, five-epoch warm-up and cosine decay on eight A100 GPUs; 384 fine-tuning uses 30 epochs.
- **Metrics/results:** FastViT-SA24 reports 82.6% top-1 without distillation at 20.6M parameters/3.8G FLOPs; SA36 reports 83.6%; MA36 reports 83.9%, rising to 84.9% at 384 resolution. The paper emphasises measured latency and robustness as well as accuracy.
- **Limitations:** structural reparameterisation increases engineering and verification burden; the larger results require A100-scale training; deployment speed depends on target hardware and kernels.
- **Code/data availability:** [official Apple FastViT repository](https://github.com/apple/ml-fastvit).
- **Practical lesson:** delay attention until low resolution and measure latency. Structural reparameterisation is out of scope unless deployment becomes the research question.

#### 19. EfficientViT: Memory Efficient Vision Transformer with Cascaded Group Attention (`8XFL6FCR`)

**Source:** [Liu et al., 2023](https://openaccess.thecvf.com/content/CVPR2023/papers/Liu_EfficientViT_Memory_Efficient_Vision_Transformer_With_Cascaded_Group_Attention_CVPR_2023_paper.pdf)

- **Architecture:** three hierarchical stages using a sandwich layout with depthwise-convolution feed-forward blocks around a single attention block. Cascaded Group Attention splits channels across heads and feeds each head information from the preceding head; parameter allocation is adjusted around memory-bound operations.
- **Convolution/attention interaction:** depthwise convolution supplies local mixing and attention is sparse in block count, targeting memory efficiency rather than only FLOPs.
- **Input representation:** overlapping patch embedding and hierarchical feature tokens.
- **Dataset and task:** ImageNet-1K classification, COCO detection/instance segmentation, and Cityscapes segmentation.
- **Training setup:** scratch training for 300 epochs on eight V100 GPUs, AdamW, batch 2,048, learning rate 0.001, weight decay 0.025, cosine schedule, and Mixup, AutoAugment, and random erasing.
- **Metrics/results:** EfficientViT-M2 reports 70.8% top-1 at 4.2M parameters/201M FLOPs; M4 reports 74.3%; M5 reports 77.1% at 12.4M/522M and high reported throughput. Higher-resolution variants improve accuracy.
- **Limitations:** head cascading introduces sequential dependencies; hand-tuned parameter allocation is less transparent; accuracy/throughput trade-offs still require measurement on the actual target device.
- **Code/data availability:** the paper links an official implementation in the Microsoft Research project repositories.
- **Practical lesson:** one attention block between local-mixing blocks is sufficient for a tiny hybrid. Avoid inventing a specialised attention operator unless standard attention is measured as the bottleneck.

#### 20. CTRL-F: Multi-Level CNN-Transformer Feature Fusion (`HKLMLZIF`)

**Source:** [El-Assiouti et al., 2025](https://arxiv.org/pdf/2407.06673)

- **Architecture:** a five-stage MBConv CNN plus a multi-level feature cross-attention Transformer. Feature maps from two CNN levels are patch-tokenised at different scales, cross-attention exchanges class-token information, and CNN/Transformer predictions are fused through adaptive or collaborative knowledge-fusion variants.
- **Convolution/attention interaction:** explicit multi-level interaction and decision fusion; local CNN features and global token representations remain separately observable.
- **Input representation:** 224×224 images; stage-two and stage-four CNN feature maps become fine- and coarse-scale tokens.
- **Dataset and task:** PlantVillage (54,303 images, 38 classes, 80/20 split), Oxford Flowers-102 (2,040 train, 6,149 test), and CUB-200-2011 (5,994 train, 5,794 test).
- **Training setup:** from scratch with AdamW, cosine schedule, initial learning rate 5×10⁻⁴, minimum 10⁻⁵, weight decay 0.05, five-epoch warm-up, batch 32, flipping/rotation, and 100 epochs for PlantVillage or 200 for Oxford/CUB on a P100.
- **Metrics/results:** CTRL-F-S with adaptive fusion reports 82.42% on Oxford, 56.27% on CUB, and 99.85% on PlantVillage at 9.97M parameters/1.43G FLOPs. CTRL-F-B with collaborative fusion reports 83.00%, 61.68%, and 99.91% at 21.39M/3.29G.
- **Limitations:** no crack experiment; multi-level cross-attention and multiple fusion losses/variants complicate a student study; results are sensitive to dataset difficulty and image resolution; the work is recent and less independently established.
- **Code/data availability:** [official CTRL-F repository](https://github.com/hosamsherif/CTRL-F).
- **Practical lesson:** separately inspectable local/global predictions are scientifically valuable. Reproduce that observability with one light fusion module, not the full multi-level network.

### 3.4 Reviews and field-level evidence

#### 21. Intelligent Eyes on Buildings: A Scientometric Mapping and Systematic Review of AI-Based Crack Detection and Predictive Diagnostics of Building Structures (`EHU23BPQ`)

**Source:** [2026 Encyclopedia review](https://www.mdpi.com/2673-8392/6/4/75)

- **Architecture:** no new classifier. The paper reviews classical vision, CNNs, YOLO families, segmentation, transfer learning, Transformers, UAV imaging, and edge deployment.
- **Convolution/attention interaction:** synthesises model-family trends rather than proposing a fusion mechanism.
- **Input representation:** reviewed studies primarily use RGB photographs; a smaller group uses UAV, thermal, point-cloud, or multimodal inputs.
- **Dataset and task:** scientometric dataset of 146 Scopus-indexed publications from 2015–2025 and a technical-review subset of 36 studies focused on building cracks.
- **Review setup:** PRISMA-style identification/screening, duplicate control by DOI/title/EID, VOSviewer 1.6.20 and spreadsheet analysis, then structured extraction of datasets, architectures, validation, metrics, hardware, open data/code, limitations, and failure cases.
- **Results/findings:** CNN and YOLO approaches dominate; segmentation and Transformers are growing; transfer learning is common for small datasets. Dataset diversity, external validation, systematic hyperparameter optimisation, open code/data, deployment reporting, predictive diagnostics, and integration with structural-health decisions remain limited.
- **Limitations:** English/Scopus/building-focused selection limits coverage; bibliometric prominence is not evidence of model quality; the technical subset is heterogeneous and cannot support a pooled performance estimate.
- **Code/data availability:** no model code is applicable; the review reports its search and extraction workflow.
- **Practical lesson:** methodological rigour is a contribution. Publish partitions, seeds, configurations, and code; evaluate a held-out domain and efficiency instead of reporting only a high random-split accuracy.

#### 22. Artificial Intelligence-Driven Intelligent Concrete Crack Detection and Real-Time Width Estimation for Smart Structural Health Monitoring Systems: A Review (`2CJMWDZT`)

**Source:** [2026 International Journal of Applied Resilience and Sustainability review](https://www.deepscipub.com/ijars/article/view/52)

- **Architecture:** no new trained model. It surveys CNN classification/detection/segmentation, Vision Transformers, vision-language models, transfer/domain adaptation, width measurement, edge AI, UAVs, IoT, and digital twins.
- **Convolution/attention interaction:** contrasts convolution's efficient local pattern extraction with attention's global context and higher computational cost; it does not test a new hybrid.
- **Input representation:** reviewed systems span ordinary RGB, calibrated close-range imagery, stereo/3D data, UAV imagery, and non-visual structural sensors.
- **Dataset and task:** narrative comparison across public crack datasets and width-estimation studies; tasks include classification, detection, segmentation, and physical width measurement.
- **Review setup:** thematic technical synthesis and comparative tables; it is not an experimental training study, so optimizer, split, and model-training fields are not applicable.
- **Results/findings:** laboratory detection is comparatively mature, but standardised benchmarks, cross-domain generalisation, field validation, hardware-software co-design, and longitudinal calibrated width measurement remain weak. It argues that transfer learning is practical for data-sparse applications and that no architecture dominates all deployment objectives.
- **Limitations:** heterogeneous tasks and metrics make table-level comparisons fragile; several claims aggregate studies with different data and operating conditions; it does not provide a reproducible meta-analysis or a new validation dataset.
- **Code/data availability:** no model code is applicable.
- **Practical lesson:** this project should explicitly state that it solves classification, not width measurement or segmentation. Its credible field contribution is cross-domain reliability and efficiency evidence, not a claim of operational structural diagnosis.

## 4. Cross-paper synthesis

### 4.1 How convolution and attention complement each other

| Function | Convolution contributes | Attention contributes | Best minimal interaction |
|---|---|---|---|
| Crack edge/texture | Strong local prior; parameter sharing; thin-line and high-frequency response | Can suppress isolated texture by considering distant context | Preserve a moderately high-resolution local map. |
| Long crack continuity | Requires depth, dilation, or large kernels to connect distant parts | Direct token-to-token dependency across the reduced map | Apply attention after the CNN stem. |
| Nuisance rejection | Local cues alone may confuse joints, shadows, stains, and roughness | Global surrounding context can distinguish a crack from a seam or boundary | Fuse local and global maps before pooling. |
| Small-data learning | CNN bias usually trains more reliably | Pure ViT is data hungry but transfer/regularisation helps | CNN-derived tokens plus pretrained or shallow attention. |
| Efficiency | Excellent kernels and linear spatial scaling | Cost grows quadratically with token count | Keep the token grid small; do not design new efficient attention prematurely. |
| Interpretability | Grad-CAM/local activation maps | Attention rollout/token relations | Preserve separate pre-fusion branch outputs for analysis. |

### 4.2 Dataset and evaluation risks

1. **Source leakage:** SDNET's 56,092 samples come from only 230 originals. Random crop splitting can make test images near-duplicates of training content. The same issue applies to the 17,000 crops from 1,000 sources in the improved Transformer paper.
2. **Class imbalance:** SDNET has roughly 5.6 non-crack crops per crack crop overall. Accuracy can be high while recall on cracks is poor.
3. **Domain imbalance:** decks, walls, and pavements have different textures, capture conditions, and crack distributions. Overall pooled performance can hide failure on one surface.
4. **Uncontrolled metric comparability:** papers mix accuracy, F1, mIoU, tolerance-aware segmentation IoU, ensembles, test-time augmentation, different resolutions, and different pretraining. Results must not be placed into a single leaderboard without qualification.
5. **Closed or incomplete reproducibility:** several papers provide no code or split manifests, and some datasets are available only on request. The proposed work should release exact split manifests and configurations.

### 4.3 Training conclusions

- Start with transfer learning when the chosen components have compatible pretrained weights; compare with scratch training only as an ablation.
- Use the same augmentation policy for matched CNN, Transformer, and hybrid models. A reasonable crack-safe policy is horizontal/vertical flips, small rotations, mild colour/brightness/contrast variation, and limited random resized crop. Avoid transformations that erase very thin cracks.
- Use early stopping/model selection strictly on validation data. Keep the test set untouched until the final run.
- Use class-weighted binary cross-entropy or balanced sampling, but do not change both simultaneously in the main experiment without an ablation.
- Report at least three seeds, mean±standard deviation, and confidence intervals or bootstrap intervals for the final test comparison if feasible.
- Calibrate the decision threshold on validation data when recall/precision trade-offs matter; also report threshold-independent ROC-AUC (and preferably PR-AUC under imbalance).

### 4.4 Efficiency and interpretability conclusions

- Parameters and MACs/FLOPs are necessary but not sufficient. MobileViT and FastViT show why latency must be measured on the actual available GPU/CPU.
- Keep input resolution and batch size fixed for latency comparison, include warm-up, and report median per-image latency and peak memory.
- Interpretability is evidence about model behaviour, not proof of causal reasoning. Show correctly classified cracks, false negatives, and nuisance-driven false positives for both branches.
- Compare CNN Grad-CAM, Transformer attention rollout, and fused-model output on the same samples. Quantitative localisation is optional unless masks are available.

## 5. Proposed research contribution

### 5.1 Research question

> **Under source-separated and cross-surface evaluation, does one explicit fusion of lightweight convolutional local features and Transformer global features improve concrete crack classification over parameter-matched CNN-only and Transformer-only baselines?**

This question is smaller and more defensible than claiming a new general-purpose architecture or state of the art. The novelty is the controlled local/global complementarity study under a leakage-resistant, domain-aware protocol.

### 5.2 Minimal proposed model: CrackFusion-Tiny (working name)

1. **Shared input and CNN stem:** 224×224 RGB input; two or three small residual/depthwise convolution stages produce a local feature map.
2. **Local branch:** one light residual/depthwise block preserves crack-edge and texture features.
3. **Global branch:** project the shared feature map to a modest embedding dimension, flatten the reduced spatial grid into tokens, add positional information, and use one or two standard Transformer encoder blocks.
4. **Alignment:** reshape global tokens back to a feature map and project local/global channels to the same width.
5. **Fusion:** concatenate once and apply a 1×1 convolution. If capacity permits one focused novelty, add a single sigmoid gate initialised near equal weighting and report its learned value/distribution.
6. **Head:** global average pooling, dropout, and one binary classifier.

No custom attention operator, repeated cross-attention bridge, structural reparameterisation, knowledge distillation, segmentation head, or architecture search is needed for the primary contribution.

### 5.3 Minimum experiment matrix

| ID | Model | Purpose |
|---|---|---|
| B1 | ResNet-18 transfer baseline | Recognisable strong CNN reference. |
| B2 | Parameter-matched small CNN using the same stem/local branch | Isolates local processing fairly. |
| B3 | Parameter-matched tiny Transformer on patches or stem tokens | Isolates global attention fairly. |
| H1 | CrackFusion-Tiny with fixed concat+1×1 fusion | Tests the hybrid hypothesis. |
| A1 | H1 without the local post-stem block | Tests whether specialised local refinement matters. |
| A2 | H1 without Transformer blocks | Confirms the global branch contribution; may coincide with B2 if parameter matching is preserved. |
| A3 | Optional gated fusion versus fixed fusion | Include only if the gate is the claimed architectural contribution. |

The primary table should keep input size, augmentation, optimizer family, epoch budget, early-stopping rule, and data splits fixed. Parameter matching should be approximate and disclosed rather than achieved through contrived layers.

### 5.4 Evaluation protocol

1. Build a manifest mapping every SDNET crop to its original source photograph and surface. If direct source identifiers are unavailable, reconstruct groups conservatively from the dataset directory/filename metadata and document the rule.
2. Create group-stratified train/validation/test splits with no source photograph crossing partitions.
3. Run a pooled source-separated experiment and three leave-one-surface-out experiments: train on two of deck/wall/pavement and test on the third.
4. Keep one final split fixed for all models; use training/validation only for tuning.
5. Report accuracy, balanced accuracy, precision, recall, specificity, F1, ROC-AUC, PR-AUC, confusion matrices, parameters, MACs/FLOPs, peak memory, and median latency.
6. Repeat the principal comparison over at least three seeds. Include per-surface results and false-negative analysis.
7. Produce matched Grad-CAM, attention-rollout, and fused-model visualisations for true positives, false negatives, and common false positives such as seams, shadows, stains, and rough texture.

### 5.5 Claim boundary

A successful paper could claim:

> A compact, explicitly fused local/global classifier was evaluated under source-separated and cross-surface concrete-crack protocols. The study quantifies when the hybrid improves recall/generalisation relative to matched single-family baselines and reports its accuracy–efficiency–interpretability trade-offs.

It should **not** claim field-ready structural diagnosis, crack-width estimation, segmentation performance, universal generalisation, or state of the art based only on a random SDNET crop split.

## 6. Design decisions

- **Primary architectural inspiration:** MobileViT for CNN-feature tokenisation and simple map-level fusion.
- **Scientific fusion reference:** Conformer and CTRL-F, simplified to one fusion point.
- **Efficient-block references:** CvT/CMT/EfficientViT for overlapping tokenisation, local depthwise mixing, and delayed attention.
- **Training reference:** DeiT for fair small-data regularisation, used selectively rather than copied wholesale.
- **CNN baselines:** ResNet-18 and a parameter-matched small CNN; MultiScaleCrackNet now supports an optional three-scale or fixed-edge-filter ablation, but its full 71-layer design need not be reproduced unless that comparison becomes central.
- **Primary dataset:** SDNET2018, split by original photograph and analysed by surface.
- **Optional external evidence:** a second classification dataset or carefully defined Omni-Crack subset, only after the core source-separated experiment is stable.
- **Smallest defensible contribution:** one explicit lightweight local/global fusion plus a rigorous leakage-resistant, cross-surface evaluation—not a large new backbone.

This review informed the experimental protocol and methodology retained in this repository.

# Research Project Handoff

**Last updated:** 2026-08-30  
**Project directory:** `/Users/activelymac/Documents/GitHub/major_project`

## Project objective

Develop a small but publishable Conv-Transformer hybrid model for image classification, with concrete-crack classification as the primary use case. The project should be realistic for one student, use accessible datasets and reproducible code, and investigate how convolutional local features and transformer attention complement one another.

The eventual methodology document must explain:

- convolutional feature extraction;
- patch/token formation and self-attention;
- the hybrid architecture and feature-fusion mechanism;
- training, transfer learning, augmentation, and evaluation;
- ablation studies and comparisons against CNN and Transformer baselines;
- accuracy, efficiency, generalization, and interpretability trade-offs.

## Current phase status

### Phase 1 — complete

The Zotero shared group library **major project** was reviewed and additional literature was searched and screened.

- Zotero library: `major project`
- Zotero library ID: `2`
- Zotero group ID: `6634536`
- Top-level records after import: `22`
- Original relevant review papers: `2`
- New records added in Phase 1: `20`
- Exact title/DOI duplicates found: none
- Zotero target was verified as editable before import.

The new records contain metadata, source links, relevance tags, topic tags, and code/PDF availability tags. New PDF files were not downloaded as local Zotero attachments; most records contain a direct PDF URL in the URL field.

### Phase 2 — complete

All 22 top-level records in the `major project` group were reviewed individually. The structured paper-by-paper extraction, cross-paper synthesis, evaluation risks, and smallest defensible research contribution are recorded in [`phase2_synthesis.md`](phase2_synthesis.md).

- Full text was read for all 22 records.
- The user supplied the previously unavailable MultiScaleCrackNet PDF on 2026-08-30. Its complete architecture, training setup, dataset protocol, numerical results, limitations, and baseline implications were added to the synthesis.
- The Zotero group was verified as editable before reading; no Zotero records were changed.

### Phase 3 — complete

The user explicitly approved Phase 3 on 2026-08-30. The Phase 2 evidence was re-validated against the primary papers and Zotero metadata, and the completed IEEE-style methodology is available at [`phase3_crackfusion_methodology.pdf`](phase3_crackfusion_methodology.pdf).

- Final PDF: 11 A4 pages, approximately 5,600 words.
- Citations: 24 numbered IEEE-style references, all cited in the text.
- Visuals: three original vector figures and six academic tables.
- Coverage: research question and hypotheses, data provenance and source-separated splitting, the proposed CrackFusion-Tiny architecture, training, baselines, ablations, metrics, cluster-level uncertainty, efficiency, cross-surface generalisation, interpretability, reproducibility, threats to validity, and an execution plan.
- Validation: every numerical or methodological literature claim used in the PDF was checked against the original paper; ambiguous or internally inconsistent claims were excluded or qualified.
- PDF QA: every page was rendered and visually inspected; no clipping, overlap, broken tables, or unreadable citations remained in the final render.

Two primary interpretability references were added to the editable `major project` Zotero group during Phase 3 after duplicate checks:

1. `STKFXPT3` — Grad-CAM: Visual Explanations from Deep Networks via Gradient-Based Localization.
2. `VQRWTCHN` — Quantifying Attention Flow in Transformers.

The group therefore contains 24 top-level records after Phase 3. No other new literature was required.

## Papers added to Zotero

### Foundations

1. `M9GHNUCF` — [Attention Is All You Need](https://papers.neurips.cc/paper/7181-attention-isall-you-need.pdf), Vaswani et al., 2017. Essential attention/Transformer background.
2. `GH8EIH8C` — [Deep Residual Learning for Image Recognition](https://openaccess.thecvf.com/content_cvpr_2016/papers/He_Deep_Residual_Learning_CVPR_2016_paper.pdf), He et al., 2016. Essential CNN/residual-learning baseline.
3. `P62GMGTN` — [An Image Is Worth 16x16 Words: Transformers for Image Recognition at Scale](https://arxiv.org/pdf/2010.11929), Dosovitskiy et al., 2021. Essential Vision Transformer background.
4. `CXTFQ3YB` — [Training Data-Efficient Image Transformers and Distillation through Attention](https://proceedings.mlr.press/v139/touvron21a/touvron21a.pdf), Touvron et al., 2021. Essential for training Transformers with limited data.

### Vision Transformers, hybrids, and efficiency

5. `GTCI5SK8` — [Swin Transformer](https://openaccess.thecvf.com/content/ICCV2021/papers/Liu_Swin_Transformer_Hierarchical_Vision_Transformer_Using_Shifted_Windows_ICCV_2021_paper.pdf), Liu et al., 2021. Hierarchical shifted-window attention; official code available.
6. `LQT8CXBK` — [CvT: Introducing Convolutions to Vision Transformers](https://openaccess.thecvf.com/content/ICCV2021/papers/Wu_CvT_Introducing_Convolutions_to_Vision_Transformers_ICCV_2021_paper.pdf), Wu et al., 2021. Convolutional token embedding and convolutional projections.
7. `GWUJX2DK` — [Conformer: Local Features Coupling Global Representations for Visual Recognition](https://openaccess.thecvf.com/content/ICCV2021/papers/Peng_Conformer_Local_Features_Coupling_Global_Representations_for_Visual_Recognition_ICCV_2021_paper.pdf), Peng et al., 2021. Explicit CNN/Transformer feature coupling; official code available.
8. `2KCLWMMZ` — [CoAtNet: Marrying Convolution and Attention for All Data Sizes](https://proceedings.neurips.cc/paper_files/paper/2021/file/20568692db622456cc42a2e853ca21f8-Paper.pdf), Dai et al., 2021. Staged convolution-plus-attention design.
9. `AGUTHS2H` — [CMT: Convolutional Neural Networks Meet Vision Transformers](https://openaccess.thecvf.com/content/CVPR2022/papers/Guo_CMT_Convolutional_Neural_Networks_Meet_Vision_Transformers_CVPR_2022_paper.pdf), Guo et al., 2022. Lightweight CNN/Transformer architecture; implementation links recorded in Zotero.
10. `UZT7VV56` — [MobileViT](https://arxiv.org/pdf/2110.02178), Mehta and Rastegari, 2022. Practical lightweight hybrid and strong candidate for modification.
11. `F38CEX55` — [Mobile-Former](https://openaccess.thecvf.com/content/CVPR2022/papers/Chen_Mobile-Former_Bridging_MobileNet_and_Transformer_CVPR_2022_paper.pdf), Chen et al., 2022. MobileNet branch bridged to a small-token Transformer using cross-attention.
12. `4YLNLIG8` — [FastViT](https://openaccess.thecvf.com/content/ICCV2023/papers/Vasu_FastViT_A_Fast_Hybrid_Vision_Transformer_Using_Structural_Reparameterization_ICCV_2023_paper.pdf), Vasu et al., 2023. Efficient hybrid architecture with structural reparameterization.
13. `8XFL6FCR` — [EfficientViT](https://openaccess.thecvf.com/content/CVPR2023/papers/Liu_EfficientViT_Memory_Efficient_Vision_Transformer_With_Cascaded_Group_Attention_CVPR_2023_paper.pdf), Liu et al., 2023. Memory-efficient attention and lightweight deployment.
14. `HKLMLZIF` — [CTRL-F](https://arxiv.org/pdf/2407.06673), El-Assiouti et al., 2025. Recent multi-level CNN/Transformer cross-attention model with public code; marked advanced.

### Concrete-crack classification and datasets

15. `UBGE2XUB` — [SDNET2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6247444/), Dorafshan et al., 2018. Important concrete-crack binary-classification dataset and benchmark paper.
16. `9RL32V4L` — [Road Crack Detection Using Deep Convolutional Neural Network](https://doi.org/10.1109/ICIP.2016.7533052), Zhang et al., 2016. Early CNN crack-classification work and dataset source.
17. `B9X3LZ38` — [CCTNet](https://www.mdpi.com/1424-8220/24/13/4257), Yadav et al., 2024. Directly relevant CNN/Transformer concrete-crack detector.
18. `WII7ZDKS` — [An Improved Transformer-Based Concrete Crack Classification Method](https://www.nature.com/articles/s41598-024-54835-x.pdf), Ye et al., 2024. Recent Transformer-based concrete-crack classifier.
19. `KU57S9P4` — [MultiScaleCrackNet](https://doi.org/10.1016/j.eswa.2024.123658), Russel and Selvaraj, 2024. Strong multiscale CNN baseline for crack classification.
20. `RBFNPZW6` — [Omni-Crack30k](https://openaccess.thecvf.com/content/CVPR2024W/VAND/papers/Benz_OmniCrack30k_A_Benchmark_for_Crack_Segmentation_and_the_Reasonable_Effectiveness_CVPRW_2024_paper.pdf), Benz and Rodehorst, 2024. Optional cross-dataset benchmark and transfer-learning reference; primarily segmentation rather than classification.

## Zotero tags used

Every added record has `phase1-screened`. Relevance is indicated with:

- `essential`
- `useful`
- `optional`

Other tags include `foundational`, `hybrid-architecture`, `cnn`, `transformer`, `lightweight`, `image-classification`, `concrete-crack`, `dataset`, `benchmark`, `code-available`, `direct-pdf`, `manual-pdf-needed`, and `no-code-found`.

## PDF follow-up status

All three previously unresolved papers are now available for Phase 2 synthesis:

1. **Road Crack Detection Using Deep Convolutional Neural Network** — resolved through the open author manuscript.
2. **SDNET2018** — resolved through the open article.
3. **MultiScaleCrackNet** — resolved through the full published PDF supplied by the user on 2026-08-30.

## Screening decisions

No top-level record already in the shared group was irrelevant; the two original records were relevant review papers. Therefore, no group record was tagged `irrelevant`.

Segmentation-only papers such as [CrackTrNet](https://www.sciencedirect.com/science/article/pii/S0926580524001766) and [A Convolutional-Transformer Network for Crack Segmentation with Boundary Awareness](https://arxiv.org/abs/2302.11728) were screened out because the immediate project target is classification. Adjacent audio, spiking-neural-network, reinforcement-learning, and unrelated medical-imaging papers were also not added to the shared group.

## Recommended next-chat instruction

Resume from the completed methodology PDF and obtain the SDNET2018 files. Before model implementation, verify whether every 256 x 256 tile can be mapped to its original parent photograph; do not claim a source-separated pooled split unless that mapping is available or reconstructed defensibly.

Before any future Zotero write, re-check that the selected target is still the editable `major project` group. Do not modify the Zotero database directly.

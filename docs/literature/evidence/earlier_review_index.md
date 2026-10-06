# Crack-Model Literature Review

**Last reviewed:** 2026-10-06\
**Search focus:** image-based crack classification, detection, and segmentation; especially CNN–Transformer hybrids and the project's SDNET2018 experiment.\
**Status:** targeted scoping review completed on 2026-10-06; counts and coverage are based on the explicitly screened corpus, not a claim that every paper ever published has been found.

## Start here

1. [MobileViT-XS baseline vs CrackFusion-Tiny](../mobilevit_baseline_and_crackfusion_comparison.md) — what our baseline code does, how MobileViT works, and how it differs from our custom model.
2. [CNN–Transformer crack-classification hybrids](../crack_classification_hybrids.md) — image-level classification papers, including direct binary and severity examples.
3. [CNN–Transformer detection and segmentation hybrids](../detection_segmentation_hybrids.md) — pixel-/object-level crack localization papers; related to the domain but different from our tile classifier.
4. [Datasets, evaluation, and research gaps](../datasets_evaluation_and_gaps.md) — dataset scope, leakage, class balance, generalization, and reporting practices.
5. [Search method, model count, and implications for our paper](../search_scope_and_research_position.md) — inclusion rules, corpus count, coverage limits, and defensible novelty wording.

## Extended evidence and reading logs

These files preserve the deeper parallel research: paper-by-paper source/access notes, broader architecture context, dataset-provenance evidence, deployment studies, and review-level positioning. The synthesis files above are the faster starting point; use these when checking a particular claim or tracing how a candidate was screened.

- [Image-level classifier evidence log](scope_classifier_evidence_log.md) — crack-presence and severity studies, their data/splits, and full-text verification limits.
- [General CNN–Transformer architecture literature](scope_hybrid_vision_architectures.md) — major vision hybrid families and which design lessons transfer to our compact model.
- [Additional detection/segmentation evidence](scope_detection_segmentation_evidence.md) — recent candidates and task-boundary details that extend the 22-paper screened list.
- [Dataset provenance and generalization evidence](scope_dataset_provenance_and_generalization.md) — parent-image mapping, split units, domain shift, uncertainty, and detailed source notes.
- [Efficiency and deployment evidence](scope_efficiency_and_deployment.md) — mobile/edge studies, reported workloads, and a reproducible measurement checklist.
- [Review papers and research positioning](scope_reviews_and_research_position.md) — recent review-level evidence, safe claims, and limits of the project Zotero snapshot.

## Fast answer to “how many?”

In this targeted screen (as of 2026-10-06), we found **5 peer-reviewed image-level crack/road-damage classifier candidates plus 1 concrete-crack classification preprint**, and **at least 22 published crack segmentation papers** meeting the stated narrow CNN–Transformer rule. Segmentation and classification counts are separate; these are paper counts in a screened corpus, not an exhaustive field census or a count of unique model variants. Read [the count definitions and limits](../search_scope_and_research_position.md) before quoting a number.

## MobileViT-XS and CrackFusion-Tiny in one sentence

Both are CNN–Transformer hybrids: MobileViT repeatedly mixes convolution and attention within one staged stream; CrackFusion-Tiny uses a shared stem, parallel local/global branches, and one final feature-map fusion. Our baseline notebook fine-tunes pretrained MobileViT-XS from `timm`; it does not implement a new MobileViT architecture. See [the detailed comparison](../mobilevit_baseline_and_crackfusion_comparison.md).

## Search vocabulary

Use these terms to search this folder: `MobileViT`, `MobileViT-XS`, `CNN-Transformer`, `hybrid`, `dual-branch`, `dual-encoder`, `parallel`, `local-global`, `feature fusion`, `cross-attention`, `crack classification`, `crack detection`, `crack segmentation`, `severity`, `SDNET2018`, `source split`, `leakage`, `cross-surface`, `domain shift`, `TinyML`, `edge deployment`, and `interpretability`.

Each paper entry records the task level, architecture/fusion pattern, dataset, evaluation split, and relevance to CrackFusion-Tiny where that information is available. Classification, object detection, and segmentation are kept separate because their outputs and evaluation metrics are different.

## Existing project material

- [Earlier broad literature synthesis](scope_existing_literature_synthesis.md)
- [Experimental protocol](../../planning/experimental_protocol.md)
- [MobileViT baseline notebook](../../../notebooks/02_mobilevit_train.ipynb)
- [CrackFusion-Tiny source](../../../notebooks/03_crackfusion_train.ipynb)
- [Zotero metadata snapshot](../references/zotero_snapshot.json)

The files in this folder consolidate the existing project review and the additional survey workstreams. Search results are split by topic so classification, localization, datasets, deployment, and general architecture evidence are not conflated.

## Search and counting rules

The paper counts in this index are **screened minimums**: distinct research papers located through targeted searches of primary publisher/conference/arXiv sources and relevant citations, whose actual method applies convolution and Transformer/self-attention components to crack imagery. A paper is counted once, even if it evaluates multiple datasets or proposes several model variants. General-purpose hybrid architecture papers are background, not crack-domain models. Papers that only mention CNN–Transformer hybrids in related work are excluded.

Results are grouped by **task** (image classification, object detection, semantic/instance segmentation) and **architecture** (serial/staged, parallel dual-branch, encoder-decoder fusion, attention/gated fusion). Preprints are marked. Reported scores from different papers are not ranked as if they came from a shared benchmark.

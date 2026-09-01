#!/usr/bin/env python3
"""Build the Phase 3 IEEE-style methodology PDF."""

from __future__ import annotations

import json
import math
import re
import unicodedata
from pathlib import Path

from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "phase3_crackfusion_methodology.pdf"
ITEMS_JSON = ROOT / "sources" / "phase3_zotero_items.json"

PAGE_W, PAGE_H = A4
MARGIN_X = 15 * mm
MARGIN_TOP = 16 * mm
MARGIN_BOTTOM = 16 * mm
GAP = 5 * mm
COL_W = (PAGE_W - 2 * MARGIN_X - GAP) / 2
FULL_W = PAGE_W - 2 * MARGIN_X

NAVY = HexColor("#17324D")
BLUE = HexColor("#2A6F97")
TEAL = HexColor("#2A9D8F")
PALE = HexColor("#EAF2F7")
PALE_TEAL = HexColor("#E7F5F2")
GOLD = HexColor("#E9C46A")
INK = HexColor("#17212B")
MID = HexColor("#52616B")
LIGHT = HexColor("#D7E0E7")
WHITE = colors.white


def ascii_text(value: str) -> str:
    value = value.replace("×", "x").replace("–", "-").replace("—", "-")
    value = value.replace("’", "'").replace("“", '"').replace("”", '"')
    return unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")


def esc(value: str) -> str:
    return ascii_text(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="PaperTitle", parent=styles["Title"], fontName="Times-Bold", fontSize=18,
    leading=20.5, alignment=TA_CENTER, textColor=NAVY, spaceAfter=7,
))
styles.add(ParagraphStyle(
    name="Subtitle", parent=styles["Normal"], fontName="Times-Roman", fontSize=10,
    leading=12, alignment=TA_CENTER, textColor=MID, spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="Abstract", parent=styles["Normal"], fontName="Times-Roman", fontSize=9.1,
    leading=11.2, alignment=TA_JUSTIFY, textColor=INK, spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="BodyIEEE", parent=styles["BodyText"], fontName="Times-Roman", fontSize=8.9,
    leading=10.8, alignment=TA_JUSTIFY, textColor=INK, firstLineIndent=10, spaceAfter=4.2,
    allowWidows=0, allowOrphans=0,
))
styles.add(ParagraphStyle(
    name="BodyNoIndent", parent=styles["BodyIEEE"], firstLineIndent=0,
))
styles.add(ParagraphStyle(
    name="SectionIEEE", parent=styles["Heading1"], fontName="Times-Bold", fontSize=10.2,
    leading=12, alignment=TA_CENTER, textColor=NAVY, spaceBefore=8, spaceAfter=5,
    keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="SubsectionIEEE", parent=styles["Heading2"], fontName="Times-BoldItalic", fontSize=9.3,
    leading=11, alignment=TA_LEFT, textColor=NAVY, spaceBefore=6, spaceAfter=3,
    keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="SubsubIEEE", parent=styles["Heading3"], fontName="Times-Italic", fontSize=9,
    leading=10.5, alignment=TA_LEFT, textColor=INK, spaceBefore=4.5, spaceAfter=2,
    keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="BulletIEEE", parent=styles["BodyNoIndent"], leftIndent=9, firstLineIndent=-6,
    bulletIndent=1, spaceAfter=2.4,
))
styles.add(ParagraphStyle(
    name="Equation", parent=styles["BodyNoIndent"], fontName="Helvetica-Oblique", fontSize=8.1,
    leading=10, alignment=TA_CENTER, leftIndent=5, rightIndent=5, spaceBefore=3, spaceAfter=4,
    backColor=HexColor("#F5F7F9"), borderColor=LIGHT, borderWidth=0.4, borderPadding=4,
))
styles.add(ParagraphStyle(
    name="Caption", parent=styles["Normal"], fontName="Times-Roman", fontSize=7.7,
    leading=9.1, alignment=TA_CENTER, textColor=INK, spaceBefore=3, spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="TableCaption", parent=styles["Caption"], fontName="Times-Bold", spaceBefore=5, spaceAfter=3,
))
styles.add(ParagraphStyle(
    name="TableCell", parent=styles["Normal"], fontName="Times-Roman", fontSize=7.4,
    leading=8.7, alignment=TA_LEFT, textColor=INK,
))
styles.add(ParagraphStyle(
    name="TableHead", parent=styles["TableCell"], fontName="Times-Bold", textColor=WHITE,
    alignment=TA_CENTER,
))
styles.add(ParagraphStyle(
    name="Ref", parent=styles["Normal"], fontName="Times-Roman", fontSize=7.35,
    leading=8.7, alignment=TA_LEFT, leftIndent=12, firstLineIndent=-12, spaceAfter=2.6,
))
styles.add(ParagraphStyle(
    name="Callout", parent=styles["BodyNoIndent"], fontName="Times-Italic", fontSize=8.6,
    leading=10.6, backColor=PALE_TEAL, borderColor=TEAL, borderWidth=0.7,
    borderPadding=7, spaceBefore=5, spaceAfter=7,
))


ORDER = [
    "EHU23BPQ", "2CJMWDZT", "UBGE2XUB", "9RL32V4L", "B9X3LZ38", "WII7ZDKS",
    "KU57S9P4", "RBFNPZW6", "GH8EIH8C", "M9GHNUCF", "P62GMGTN", "CXTFQ3YB",
    "GTCI5SK8", "LQT8CXBK", "GWUJX2DK", "2KCLWMMZ", "AGUTHS2H", "UZT7VV56",
    "F38CEX55", "4YLNLIG8", "8XFL6FCR", "HKLMLZIF", "STKFXPT3", "VQRWTCHN",
]
REFNO = {key: i + 1 for i, key in enumerate(ORDER)}


def cite(*keys: str) -> str:
    nums = sorted({REFNO[k] for k in keys})
    groups = []
    start = prev = nums[0]
    for n in nums[1:]:
        if n == prev + 1:
            prev = n
            continue
        groups.append(str(start) if start == prev else f"{start}-{prev}")
        start = prev = n
    groups.append(str(start) if start == prev else f"{start}-{prev}")
    return "[" + ", ".join(groups) + "]"


def P(text: str, style: str = "BodyIEEE") -> Paragraph:
    return Paragraph(esc(text), styles[style])


def PH(text: str, style: str = "BodyIEEE") -> Paragraph:
    """Paragraph with trusted ReportLab markup and ASCII-normalized text."""
    return Paragraph(ascii_text(text), styles[style])


def S(title: str, roman: str) -> Paragraph:
    return Paragraph(f"{roman}. {esc(title.upper())}", styles["SectionIEEE"])


def SS(title: str, letter: str) -> Paragraph:
    return Paragraph(f"{letter}. {esc(title)}", styles["SubsectionIEEE"])


def SSS(title: str, number: str) -> Paragraph:
    return Paragraph(f"{number}) {esc(title)}", styles["SubsubIEEE"])


def B(text: str) -> Paragraph:
    return Paragraph(f"- {esc(text)}", styles["BulletIEEE"])


def Eq(text: str, number: int | None = None) -> Paragraph:
    suffix = f"     ({number})" if number is not None else ""
    return Paragraph(esc(text + suffix), styles["Equation"])


def table(data, widths, header=True, font_size=7.4, aligns=None, repeat=1):
    rows = []
    for r, row in enumerate(data):
        out = []
        for c, value in enumerate(row):
            sty = "TableHead" if header and r == 0 else "TableCell"
            if aligns and c < len(aligns):
                sty_obj = ParagraphStyle(f"tmp-{r}-{c}", parent=styles[sty], alignment=aligns[c])
                out.append(Paragraph(esc(str(value)), sty_obj))
            else:
                out.append(Paragraph(esc(str(value)), styles[sty]))
        rows.append(out)
    t = Table(rows, colWidths=widths, repeatRows=repeat if header else 0, hAlign="CENTER")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3.3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.3),
        ("GRID", (0, 0), (-1, -1), 0.35, LIGHT),
    ]
    if header:
        commands.extend([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("LINEBELOW", (0, 0), (-1, 0), 0.8, NAVY),
        ])
        if len(rows) > 1:
            commands.append(("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, HexColor("#F6F8FA")]))
    t.setStyle(TableStyle(commands))
    return t


def arrow(d, x1, y1, x2, y2, color=MID, width=1.2):
    d.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=width))
    angle = math.atan2(y2 - y1, x2 - x1)
    size = 5
    pts = []
    for a in (angle + math.pi * 0.83, angle - math.pi * 0.83):
        pts.extend([x2 + size * math.cos(a), y2 + size * math.sin(a)])
    d.add(Polygon([x2, y2] + pts, fillColor=color, strokeColor=color))


def box(d, x, y, w, h, title, body="", fill=PALE, stroke=BLUE, title_size=8.5, body_size=6.8):
    d.add(Rect(x, y, w, h, rx=5, ry=5, fillColor=fill, strokeColor=stroke, strokeWidth=1))
    d.add(String(x + w / 2, y + h - 12, ascii_text(title), fontName="Helvetica-Bold",
                 fontSize=title_size, fillColor=NAVY, textAnchor="middle"))
    if body:
        lines = body.split("\n")
        for i, line in enumerate(lines):
            d.add(String(x + w / 2, y + h - 24 - i * 9, ascii_text(line), fontName="Helvetica",
                         fontSize=body_size, fillColor=INK, textAnchor="middle"))


def evidence_figure(width=FULL_W, height=245):
    d = Drawing(width, height)
    box(d, 0, 165, 110, 63, "Crack evidence", "SDNET, CCTNet,\nCSW-S, MultiScale", PALE_TEAL, TEAL)
    box(d, 0, 82, 110, 63, "Hybrid evidence", "CvT, Conformer, CMT,\nMobileViT, CTRL-F", PALE, BLUE)
    box(d, 0, 0, 110, 63, "Evaluation evidence", "Omni-Crack30k and\nsystematic reviews", HexColor("#FFF5DB"), GOLD)
    box(d, 195, 165, 125, 63, "Local design", "Depthwise residual CNN\nand overlapping tokens", PALE_TEAL, TEAL)
    box(d, 195, 82, 125, 63, "Global design", "Two compact attention\nblocks at 14 x 14", PALE, BLUE)
    box(d, 195, 0, 125, 63, "Validity design", "Parent-group splits,\nheld-out surfaces", HexColor("#FFF5DB"), GOLD)
    box(d, 395, 82, 120, 86, "CrackFusion-Tiny", "One explicit fusion\nMatched ablations\nAccuracy + efficiency\nInterpretability", HexColor("#EEF1FA"), NAVY)
    for ya, yb in ((196, 196), (113, 113), (31, 31)):
        arrow(d, 111, ya, 194, yb)
    arrow(d, 321, 196, 394, 145)
    arrow(d, 321, 113, 394, 125)
    arrow(d, 321, 31, 394, 103)
    d.add(String(width / 2, 236, "Evidence-to-design traceability", fontName="Helvetica-Bold",
                 fontSize=11, fillColor=NAVY, textAnchor="middle"))
    return d


def architecture_figure(width=FULL_W, height=335):
    d = Drawing(width, height)
    d.add(String(width / 2, height - 12, "Proposed CrackFusion-Tiny architecture", fontName="Helvetica-Bold",
                 fontSize=11, fillColor=NAVY, textAnchor="middle"))
    box(d, 15, 252, 100, 48, "Input", "224 x 224 x 3", HexColor("#F8FAFC"), MID)
    box(d, 150, 245, 130, 62, "Shared CNN stem", "Conv 3 x 3, stride 2\nDS-residual stages\n28 x 28 x 64", PALE_TEAL, TEAL)
    arrow(d, 115, 276, 149, 276)

    box(d, 45, 145, 150, 72, "Local branch", "2 DS-residual blocks\n28 x 28 x 96\nAverage pool -> 14 x 14", PALE_TEAL, TEAL)
    box(d, 320, 145, 170, 72, "Global branch", "Overlapping Conv 3 x 3, s=2\n196 tokens, d=96\n2 encoders, 4 heads", PALE, BLUE)
    arrow(d, 205, 245, 120, 218)
    arrow(d, 225, 245, 405, 218)
    box(d, 45, 75, 150, 45, "Local projection", "1 x 1 Conv -> 14 x 14 x 96", PALE_TEAL, TEAL)
    box(d, 320, 75, 170, 45, "Token reshape", "196 x 96 -> 14 x 14 x 96", PALE, BLUE)
    arrow(d, 120, 145, 120, 121)
    arrow(d, 405, 145, 405, 121)
    box(d, 180, 15, 180, 48, "Explicit fusion and head", "Concat -> 1 x 1 Conv -> GAP\nDropout -> binary logit", HexColor("#EEF1FA"), NAVY)
    arrow(d, 120, 75, 215, 63)
    arrow(d, 405, 75, 325, 63)
    d.add(String(270, 2, "Primary fusion is fixed concat + 1 x 1 convolution; adaptive gating is an ablation.",
                 fontName="Helvetica-Oblique", fontSize=7.2, fillColor=MID, textAnchor="middle"))
    return d


def evaluation_figure(width=FULL_W, height=280):
    d = Drawing(width, height)
    d.add(String(width / 2, height - 12, "Leakage-resistant experimental and evaluation flow", fontName="Helvetica-Bold",
                 fontSize=11, fillColor=NAVY, textAnchor="middle"))
    box(d, 5, 188, 110, 58, "Dataset audit", "Labels, corrupt files,\nparent IDs, duplicates", PALE_TEAL, TEAL)
    box(d, 140, 188, 120, 58, "Locked manifests", "Parent-grouped 70/15/15\nand surface metadata", PALE, BLUE)
    box(d, 285, 188, 110, 58, "Training only", "Augmentation, weights,\nhyperparameter search", PALE, BLUE)
    box(d, 420, 188, 95, 58, "Final test", "No tuning; three seeds;\ncluster bootstrap", HexColor("#FFF5DB"), GOLD)
    arrow(d, 115, 217, 139, 217)
    arrow(d, 260, 217, 284, 217)
    arrow(d, 395, 217, 419, 217)

    box(d, 35, 92, 135, 64, "Pooled source-separated", "Train/validation/test contain\nno common parent photo", PALE_TEAL, TEAL)
    box(d, 195, 92, 135, 64, "Leave-one-surface-out", "Deck | wall | pavement\nheld out in three rotations", PALE_TEAL, TEAL)
    box(d, 355, 92, 135, 64, "Optional external stress test", "No tuning on external data;\nreport label/domain mismatch", PALE_TEAL, TEAL)
    arrow(d, 260, 188, 105, 157)
    arrow(d, 260, 188, 262, 157)
    arrow(d, 260, 188, 422, 157)
    box(d, 90, 0, 335, 66, "Joint outcome report", "Balanced accuracy, recall, precision, F1, ROC-AUC, PR-AUC,\ncalibration, parameters, MACs, latency, memory,\nand branch-specific explanations", HexColor("#EEF1FA"), NAVY, body_size=6.5)
    arrow(d, 105, 92, 180, 67)
    arrow(d, 262, 92, 262, 67)
    arrow(d, 422, 92, 345, 67)
    return d


class MethodologyDoc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(filename, pagesize=A4, leftMargin=MARGIN_X, rightMargin=MARGIN_X,
                         topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM,
                         title="Methodology for a Compact Convolution-Transformer Hybrid for Concrete Crack Classification",
                         author="Major Project")
        usable_h = PAGE_H - MARGIN_TOP - MARGIN_BOTTOM
        first = Frame(MARGIN_X, MARGIN_BOTTOM, FULL_W, usable_h, id="first", leftPadding=0, rightPadding=0)
        left = Frame(MARGIN_X, MARGIN_BOTTOM, COL_W, usable_h, id="left", leftPadding=0, rightPadding=4)
        right = Frame(MARGIN_X + COL_W + GAP, MARGIN_BOTTOM, COL_W, usable_h, id="right", leftPadding=4, rightPadding=0)
        full = Frame(MARGIN_X, MARGIN_BOTTOM, FULL_W, usable_h, id="full", leftPadding=0, rightPadding=0)
        self.addPageTemplates([
            PageTemplate(id="First", frames=[first], onPage=self.page_decoration),
            PageTemplate(id="TwoCol", frames=[left, right], onPage=self.page_decoration),
            PageTemplate(id="OneCol", frames=[full], onPage=self.page_decoration),
        ])

    @staticmethod
    def page_decoration(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(LIGHT)
        canvas.setLineWidth(0.45)
        canvas.line(MARGIN_X, 10.5 * mm, PAGE_W - MARGIN_X, 10.5 * mm)
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(MID)
        canvas.drawString(MARGIN_X, 6.5 * mm, "Major Project - Phase 3 Methodology")
        canvas.drawRightString(PAGE_W - MARGIN_X, 6.5 * mm, f"Page {doc.page}")
        if doc.page > 1:
            canvas.setFont("Helvetica-Oblique", 6.8)
            canvas.drawString(MARGIN_X, PAGE_H - 9.5 * mm, "Compact Conv-Transformer Concrete Crack Classification")
            canvas.drawRightString(PAGE_W - MARGIN_X, PAGE_H - 9.5 * mm, "IEEE-style methodology")
        canvas.restoreState()


def author_ieee(creators):
    names = []
    for c in creators:
        first = c.get("firstName", "")
        last = c.get("lastName", "")
        initials = " ".join(part[0].upper() + "." for part in re.findall(r"[A-Za-z]+", first))
        names.append((initials + " " + last).strip())
    if len(names) > 6:
        return names[0] + " et al."
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + ", and " + names[-1]


def reference_text(item, n):
    data = item["data"]
    authors = author_ieee(data.get("creators", []))
    title = ascii_text(data.get("title", ""))
    venue = ascii_text(data.get("publicationTitle") or data.get("proceedingsTitle") or "")
    year_match = re.search(r"\d{4}", data.get("date", ""))
    year = year_match.group(0) if year_match else "n.d."
    parts = [f"[{n}] {authors}, \"{title},\""]
    if venue:
        parts.append(f" <i>{venue}</i>")
    volume = data.get("volume")
    issue = data.get("issue")
    pages = ascii_text(data.get("pages", ""))
    if volume:
        parts.append(f", vol. {volume}")
    if issue:
        parts.append(f", no. {issue}")
    if pages:
        if pages.isdigit() and len(pages) > 4:
            parts.append(f", Art. no. {pages}")
        else:
            parts.append(f", pp. {pages}")
    parts.append(f", {year}")
    doi = data.get("DOI")
    url = data.get("url")
    if doi:
        parts.append(f", doi: {ascii_text(doi)}")
    elif url and not venue:
        parts.append(f". [Online]. Available: {ascii_text(url)}")
    parts.append(".")
    return "".join(parts)


def build_story(items):
    story = []
    # Title page / IEEE first page
    story.append(Spacer(1, 6 * mm))
    story.append(P("Methodology for a Compact Convolution-Transformer Hybrid for Source-Separated Concrete Crack Classification", "PaperTitle"))
    story.append(P("Major Project - Phase 3 Research Methodology | 30 August 2026", "Subtitle"))
    story.append(Spacer(1, 2 * mm))
    abstract = (
        "Abstract - This document specifies a reproducible methodology for testing whether explicit fusion of "
        "convolutional local features and Transformer global features improves concrete crack classification. "
        "The design follows a re-validation of 22 primary and review papers from the project library, augmented by "
        "the original Grad-CAM and attention-rollout papers for interpretability. The proposed CrackFusion-Tiny model "
        "uses a compact residual/depthwise CNN, convolutional feature-token formation, two small self-attention blocks, "
        "and a single inspectable fusion operation. The primary dataset is SDNET2018, but its 56,092 tiles originate "
        "from only 230 photographs and are strongly imbalanced; therefore, parent-photograph grouping, locked split "
        "manifests, balanced metrics, leave-one-surface-out testing, and cluster-level uncertainty are mandatory. "
        "The study compares parameter-matched CNN-only, Transformer-only, serial hybrid, and fused hybrid models, "
        "together with a standard ResNet-18 transfer baseline. It reports accuracy, sensitivity, specificity, F1, "
        "ROC-AUC, PR-AUC, calibration, parameter count, operations, memory, latency, and branch-specific explanations. "
        "The contribution is deliberately bounded: controlled evidence about local-global complementarity and "
        "cross-surface generalisation, not a claim of field-ready diagnosis or crack-width estimation."
    )
    story.append(PH(f"<b>Abstract -</b> {abstract.split('Abstract - ',1)[1]}", "Abstract"))
    story.append(PH("<b>Index Terms -</b> concrete crack classification, convolutional neural network, Vision Transformer, feature fusion, SDNET2018, generalisation, interpretability.", "Abstract"))
    story.append(Spacer(1, 2 * mm))
    status = table([
        ["Document status", "Proposed methodology; no experimental results are claimed"],
        ["Primary question", "Does one explicit local-global fusion improve source-separated and cross-surface classification?"],
        ["Primary dataset", "SDNET2018: 56,092 tiles from 230 original photographs"],
        ["Target model", "CrackFusion-Tiny, approximately 1-3M parameters (exact count to be measured)"],
    ], [38 * mm, FULL_W - 38 * mm], header=False)
    story.append(status)
    story.append(Spacer(1, 5 * mm))
    story.append(PH(
        "<b>Research contribution statement.</b> The proposed contribution is a leakage-resistant, parameter-aware "
        "evaluation of a minimal local-global fusion model. Architectural novelty is intentionally limited to one "
        "explicit fusion site so that causal ablations remain interpretable.", "Callout"))
    story.append(NextPageTemplate("TwoCol"))
    story.append(PageBreak())

    # I. Introduction
    story.append(S("Introduction", "I"))
    story.append(PH(
        f"Automated crack recognition is attractive because manual inspection is subjective, labour intensive, and "
        f"difficult to scale. Recent reviews nevertheless show that controlled in-domain accuracy has advanced faster "
        f"than external validation, predictive diagnostics, and field deployment {cite('EHU23BPQ','2CJMWDZT')}. "
        "This gap changes the objective of a student-scale project: the strongest contribution is not the largest "
        "architecture, but a transparent experiment that establishes whether local and global representations provide "
        "complementary evidence under realistic partitioning."))
    story.append(PH(
        f"Convolution encodes locality, translation structure, and parameter sharing, as exemplified by residual CNNs "
        f"{cite('GH8EIH8C')}. Self-attention directly relates distant tokens and supplies global context "
        f"{cite('M9GHNUCF')}, but the original Vision Transformer has weaker image-specific inductive bias and benefits "
        f"strongly from large-scale pretraining {cite('P62GMGTN')}. Data-efficient training {cite('CXTFQ3YB')} and "
        f"hybrid designs {cite('LQT8CXBK','GWUJX2DK','AGUTHS2H','UZT7VV56')} indicate that a small model can combine "
        "these strengths without reproducing a full industrial backbone."))
    story.append(SS("Objectives and scope", "A"))
    for text in [
        "Design one compact Conv-Transformer classifier whose local and global paths can be ablated independently.",
        "Prevent source-image leakage and expose cross-surface domain shift in SDNET2018.",
        "Compare predictive quality, efficiency, generalisation, and interpretability under fixed protocols.",
        "Release enough information for exact reproduction: manifests, seeds, configurations, logs, and model states.",
    ]:
        story.append(B(text))
    story.append(P("Segmentation, localisation, physical crack-width measurement, structural severity assessment, and operational safety decisions are outside the primary task. They may be future extensions but must not be inferred from binary image labels."))
    story.append(SS("Research question and hypotheses", "B"))
    story.append(PH("<b>RQ:</b> Under parent-source-separated and cross-surface evaluation, does one explicit fusion of lightweight convolutional local features and Transformer global features improve concrete crack classification over parameter-matched single-family baselines?", "BodyNoIndent"))
    story.append(B("H1: the fused hybrid improves mean parent-cluster F1 and PR-AUC over both matched CNN-only and Transformer-only baselines."))
    story.append(B("H2: parent-grouped performance is lower but more credible than a random tile split because correlated tiles no longer cross partitions."))
    story.append(B("H3: performance drops when deck, wall, or pavement is held out; fusion reduces the average drop relative to matched baselines."))
    story.append(B("H4: the hybrid incurs higher latency than the matched CNN, but remains within the predeclared small-model budget and offers a measurable generalisation benefit."))

    # II. Evidence validation
    story.append(S("Evidence Re-Validation and Design Rationale", "II"))
    story.append(SS("Audit procedure", "A"))
    story.append(P(
        "Every factual quantity used in this methodology was checked against the full primary paper rather than copied from the Phase 2 synthesis. Zotero metadata were reconciled with article titles, creators, years, venues, pages, and DOI/official URLs. Architecture, dataset, split, training, and result claims were checked in the methods, tables, figures, and appendices. Where a paper is ambiguous or internally inconsistent, this document either excludes the disputed value or states the uncertainty explicitly."))
    story.append(PH(
        f"Two interpretability sources were added during this audit: the original Grad-CAM paper {cite('STKFXPT3')} "
        f"and the original attention-rollout/flow paper {cite('VQRWTCHN')}. Review articles are used for field-level gaps "
        f"{cite('EHU23BPQ','2CJMWDZT')}; model and dataset facts are grounded in the corresponding primary sources."))
    story.append(SS("Validated findings that control the design", "B"))
    story.append(PH(
        f"SDNET2018 contains 56,092 RGB tiles of 256 x 256 pixels, but these were generated from only 230 photographs: "
        f"54 decks, 72 walls, and 104 pavements {cite('UBGE2XUB')}. Its 8,484 crack tiles and 47,608 non-crack tiles "
        "create substantial imbalance. Consequently, a random tile split and accuracy-only reporting are rejected."))
    story.append(PH(
        f"The early road-crack CNN achieved F1=0.8965 on a very large patch set {cite('9RL32V4L')}, while recent crack "
        f"models report high in-domain results: CCTNet reports 99.24% accuracy on SDNET walls and 97.79% on a separate "
        f"bridge subset {cite('B9X3LZ38')}; CSW-S reports 96.92% on 17,000 controlled pavement crops "
        f"{cite('WII7ZDKS')}. These values are not directly comparable because their sources, splits, inputs, and training differ."))
    story.append(PH(
        f"MultiScaleCrackNet is particularly instructive. Its combined fixed-plus-learned CNN reaches 99.6% on the "
        f"balanced Concrete Crack Images dataset, but crack recall on SDNET deck, pavement, and wall subsets falls to "
        f"33.8%, 54.4%, and 58.4%, respectively {cite('KU57S9P4')}. Omni-Crack30k independently demonstrates how "
        f"duplicates and dataset overlap can undermine evaluation {cite('RBFNPZW6')}. Therefore, the methodology treats "
        "minority-class recall, provenance, and held-out domains as first-class outcomes."))
    story.append(PH(
        f"Hybrid evidence supports reduced-resolution attention and explicit fusion. Swin restricts attention to shifted "
        f"windows {cite('GTCI5SK8')}; CvT uses convolutional token embedding and projections {cite('LQT8CXBK')}; "
        f"Conformer couples concurrent CNN and Transformer branches {cite('GWUJX2DK')}; CoAtNet places convolution "
        f"before attention {cite('2KCLWMMZ')}; and CMT mixes depthwise local processing with reduced attention "
        f"{cite('AGUTHS2H')}. MobileViT provides the most economical feature-token-folding template "
        f"{cite('UZT7VV56')}. Mobile-Former and CTRL-F provide more elaborate bidirectional or multi-level fusion "
        f"{cite('F38CEX55','HKLMLZIF')}, while FastViT and EfficientViT show that measured latency and memory matter "
        f"beyond FLOPs {cite('4YLNLIG8','8XFL6FCR')}."))

    story.append(NextPageTemplate("OneCol"))
    story.append(PageBreak())
    story.append(S("Validated Evidence Ledger", "III"))
    story.append(P("Table I records the evidence that materially changes the proposed experiment. Reported numbers remain source-specific and are not treated as a common leaderboard.", "BodyNoIndent"))
    story.append(Paragraph("TABLE I. PRIMARY EVIDENCE USED TO FIX METHODOLOGICAL CHOICES", styles["TableCaption"]))
    evidence_rows = [
        ["Ref.", "Verified source fact", "Methodological consequence"],
        [cite('UBGE2XUB'), "56,092 tiles from 230 originals; 8,484 crack vs. 47,608 non-crack", "Group by parent photograph; use imbalance-aware metrics and loss."],
        [cite('9RL32V4L'), "Patch CNN: precision 0.8696, recall 0.9251, F1 0.8965", "Recall is a primary safety-oriented metric; patch count is not independent sample count."],
        [cite('B9X3LZ38'), "CCTNet: 99.24% SDNET-wall accuracy; 97.79% separate-bridge accuracy", "Report an unseen domain, not only cross-validation."],
        [cite('WII7ZDKS'), "CSW-S: 96.92% accuracy on 17,000 pavement crops; controlled conditions", "Do not reproduce directional attention unless it beats a simpler block under nuisance-rich data."],
        [cite('KU57S9P4'), "Compact 1.3M CNN; SDNET crack recall only 33.8-58.4%", "Accuracy can conceal minority failure; multiscale/fixed-edge processing is an ablation."],
        [cite('RBFNPZW6'), "30,017-image benchmark exposes duplicates, overlap, and difficult in-the-wild subsets", "Create manifests, duplicate checks, and source-specific reports."],
        [cite('P62GMGTN','CXTFQ3YB'), "Pure ViT is data-hungry; strong augmentation/distillation improves data efficiency", "Use a small Transformer and equal augmentation budgets; distillation is optional."],
        [cite('LQT8CXBK','AGUTHS2H','UZT7VV56'), "Convolutional tokens and reduced-resolution attention preserve locality efficiently", "Form tokens from CNN features at 14 x 14 rather than raw full-resolution patches."],
        [cite('GWUJX2DK','HKLMLZIF'), "Explicit local/global branches improve observability but repeated coupling is complex", "Use one fusion point and preserve pre-fusion branch outputs."],
        [cite('4YLNLIG8','8XFL6FCR'), "FLOPs do not fully predict device latency or memory traffic", "Measure wall-clock latency and peak memory on declared hardware."],
        [cite('EHU23BPQ','2CJMWDZT'), "External validation, field testing, and cross-domain generalisation remain weak", "Make leave-one-surface-out and limitations central to the paper."],
    ]
    story.append(table(evidence_rows, [18 * mm, 75 * mm, FULL_W - 93 * mm]))
    story.append(Spacer(1, 4 * mm))
    story.append(evidence_figure())
    story.append(Paragraph("Fig. 1. Traceability from the validated literature to the minimum proposed architecture and evaluation protocol.", styles["Caption"]))
    story.append(NextPageTemplate("TwoCol"))
    story.append(PageBreak())

    # IV Dataset
    story.append(S("Dataset and Data Governance", "IV"))
    story.append(SS("Primary dataset", "A"))
    story.append(PH(
        f"SDNET2018 is selected because it is open, directly relevant, and contains three concrete-surface domains with "
        f"real nuisances such as shadows, roughness, holes, scaling, and debris {cite('UBGE2XUB')}. Each tile is RGB "
        "and 256 x 256 pixels. Images will be resized to 224 x 224 for model input; the untouched 256 x 256 files remain the archival source."))
    counts = [
        ["Surface", "Crack", "Non-crack", "Total"],
        ["Deck", "2,025", "11,595", "13,620"],
        ["Wall", "3,851", "14,287", "18,138"],
        ["Pavement", "2,608", "21,726", "24,334"],
        ["Total", "8,484", "47,608", "56,092"],
    ]
    story.append(Paragraph("TABLE II. VERIFIED SDNET2018 CLASS DISTRIBUTION", styles["TableCaption"]))
    story.append(table(counts, [24 * mm, 18 * mm, 22 * mm, 20 * mm]))
    story.append(SS("Mandatory provenance audit", "B"))
    for text in [
        "Compute SHA-256 for every file; remove exact duplicates before splitting and log every exclusion.",
        "Check image readability, dimensions, colour channels, label-folder consistency, and duplicate filenames.",
        "Recover or construct a parent-photograph identifier for every tile. If the archive does not preserve lineage, request the mapping/original images or document the limitation; a tile-random split must not be described as source-separated.",
        "Freeze a CSV manifest containing file path, hash, class, surface, parent ID, split, and exclusion reason before training.",
        "Inspect a stratified sample from each class/surface and all ambiguous/corrupt cases; retain an audit log rather than silently deleting data.",
    ]:
        story.append(B(text))
    story.append(SS("Partition strategy", "C"))
    story.append(P("The principal pooled experiment uses a group-stratified 70/15/15 train/validation/test partition. All tiles from one parent photograph are assigned to exactly one partition. Group allocation should approximately preserve crack prevalence and surface composition, but preventing parent overlap has priority over exact proportions."))
    story.append(P("Three leave-one-surface-out experiments provide the main generalisation test: train on two surfaces, select models using validation groups from those surfaces, and evaluate once on the untouched third surface. No threshold, augmentation, or hyperparameter may be chosen using the held-out surface."))
    story.append(SS("Optional external stress test", "D"))
    story.append(P("After the SDNET protocol is frozen, one public crack/no-crack dataset may be used as a zero-tuning external test. Label definitions, image source, resolution, and class balance must be documented. External data must not be mixed into training for the primary claim. Omni-Crack30k is segmentation-oriented and should only be converted to classification if the conversion rule is predeclared and preserves its official test subsets."))
    story.append(SS("Preprocessing and augmentation", "E"))
    story.append(P("Decode RGB, resize the shorter side conservatively, and take a 224 x 224 crop. Estimate channel mean and standard deviation from training images only for scratch models; use ImageNet normalization for pretrained baselines. Validation and test transformations are deterministic."))
    story.append(P("Training augmentation is intentionally mild: horizontal and vertical flips, rotations within +/-15 degrees, brightness/contrast jitter within +/-15%, and random resized crop with scale 0.85-1.00. Each operation and probability is logged. Strong erasing or aggressive crops are excluded from the primary recipe because they can remove thin cracks; CutMix/Mixup are reserved for a secondary augmentation ablation inspired by DeiT."))

    # V architecture
    story.append(S("Proposed CrackFusion-Tiny Architecture", "V"))
    story.append(SS("Design constraints", "A"))
    story.append(P("The model must be small enough for a single student to implement, train, and ablate; must expose local and global branch outputs; and must avoid a custom attention operator unless standard attention is measured as a bottleneck. The target is approximately 1-3M trainable parameters and a 14 x 14 token grid. Exact parameters, operations, and latency are reported from the implemented graph rather than estimated in the paper."))
    story.append(SS("Shared convolutional stem", "B"))
    story.append(P("A 3 x 3 stride-2 convolution maps the input to 112 x 112 x 32. Two depthwise-separable residual stages downsample to 56 x 56 x 48 and 28 x 28 x 64. Each stage uses depthwise 3 x 3 spatial convolution, pointwise 1 x 1 channel mixing, batch normalisation, GELU, and a projection shortcut only when shape changes. Residual learning follows the optimisation principle established by ResNet, while depthwise local mixing follows lightweight hybrid practice."))
    story.append(Eq("DSConv(X) = Conv_1x1( GELU( BN( DWConv_3x3(X) ) ) )", 1))
    story.append(SS("Local branch", "C"))
    story.append(P("Two residual depthwise-separable blocks map the shared 28 x 28 x 64 tensor to 28 x 28 x 96. A 2 x 2 average pool aligns it to 14 x 14 x 96. This branch retains high-frequency edges and nearby texture relationships without requiring deep receptive-field growth."))
    story.append(SS("Global branch and token formation", "D"))
    story.append(PH(
        f"An overlapping 3 x 3 stride-2 convolution maps the shared feature map to 14 x 14 x 96, following the "
        f"convolutional-token principle in CvT and MobileViT {cite('LQT8CXBK','UZT7VV56')}. The spatial grid is flattened "
        "to N=196 tokens of dimension d=96. A learnable two-dimensional positional embedding is added. Two pre-normalised Transformer encoders use four heads, MLP ratio 2, attention dropout 0.1, and stochastic depth no greater than 0.1."))
    story.append(Eq("t_i = vec(F_g[i]) W_e + p_i,    i = 1,...,196", 2))
    story.append(Eq("Attention(Q,K,V) = softmax( Q K^T / sqrt(d_k) ) V", 3))
    story.append(Eq("Z'_l = Z_(l-1) + MSA( LN(Z_(l-1)) );   Z_l = Z'_l + MLP( LN(Z'_l) )", 4))
    story.append(SS("Explicit fusion and classifier", "E"))
    story.append(P("Global tokens are reshaped to 14 x 14 x 96. Local and global maps are concatenated along channels, projected by a 1 x 1 convolution to 128 channels, globally averaged, regularised with dropout 0.2, and mapped to one binary logit. This single fusion point is deliberately simpler than repeated Conformer, Mobile-Former, or CTRL-F coupling."))
    story.append(Eq("F_f = Conv_1x1( concat(F_local, F_global) );   logit = W_c GAP(F_f) + b_c", 5))
    story.append(P("An adaptive fusion gate is not part of the primary model. It is a prespecified ablation: a channel gate generated from pooled local/global features forms g * F_local + (1-g) * F_global. This prevents the primary claim from depending on an additional mechanism whose gain could be reproduced by ordinary projection weights."))

    story.append(NextPageTemplate("OneCol"))
    story.append(PageBreak())
    story.append(S("Architecture Specification", "VI"))
    story.append(architecture_figure())
    story.append(Paragraph("Fig. 2. Proposed CrackFusion-Tiny. Tensor sizes are prespecified targets and must be confirmed from the implemented graph.", styles["Caption"]))
    arch_rows = [
        ["Component", "Operation", "Output", "Purpose"],
        ["Input", "RGB resize/crop", "224 x 224 x 3", "Common input for every model"],
        ["Stem 1", "Conv 3 x 3, s=2, 32", "112 x 112 x 32", "Early local edges"],
        ["Stem 2", "DS-residual, s=2, 48", "56 x 56 x 48", "Efficient local hierarchy"],
        ["Stem 3", "DS-residual, s=2, 64", "28 x 28 x 64", "Shared representation"],
        ["Local", "2 x DS-residual, 96; avg pool", "14 x 14 x 96", "Texture and crack continuity"],
        ["Tokens", "Overlapping Conv 3 x 3, s=2", "196 x 96", "Local-biased token formation"],
        ["Global", "2 encoders; 4 heads; MLP=192", "196 x 96", "Long-range context"],
        ["Fusion", "Concat + Conv 1 x 1, 128", "14 x 14 x 128", "One inspectable interaction"],
        ["Head", "GAP + dropout 0.2 + linear", "1 logit", "Binary crack probability"],
    ]
    story.append(Paragraph("TABLE III. PRESPECIFIED CRACKFUSION-TINY TENSOR PLAN", styles["TableCaption"]))
    story.append(table(arch_rows, [29 * mm, 56 * mm, 34 * mm, FULL_W - 119 * mm]))
    story.append(Spacer(1, 4 * mm))
    story.append(PH(
        "<b>Implementation gate.</b> If the implemented primary model exceeds 3M parameters or standard attention at "
        "196 tokens exceeds the declared memory budget, reduce channel width before changing the attention mechanism. "
        "This preserves the research question and avoids speculative complexity.", "Callout"))
    story.append(NextPageTemplate("TwoCol"))
    story.append(PageBreak())

    # VII Baselines and ablations
    story.append(S("Baselines and Ablation Design", "VII"))
    story.append(SS("Baseline families", "A"))
    story.append(P("All matched models use 224 x 224 input, the same split manifests, loss family, augmentation, training budget, and seed set. Width/depth may be adjusted once before the test is opened to keep trainable parameters within +/-10% of CrackFusion-Tiny."))
    for text in [
        "B0 - ResNet-18 transfer baseline: a recognised ImageNet-pretrained CNN reference. It is reported separately because it is not parameter matched.",
        "B1 - matched CNN-only: shared stem plus local branch, fusion-width projection, global pooling, and classifier; no tokenisation or attention.",
        "B2 - matched Transformer-only: 16 x 16 raw patches, d=96, two to four encoders as required for matching; no convolution except patch projection.",
        "B3 - serial hybrid: shared stem and Transformer branch followed directly by pooling; no local bypass or explicit fusion.",
        "H1 - CrackFusion-Tiny: local branch and global branch with one concat-plus-1 x 1 fusion.",
    ]:
        story.append(B(text))
    story.append(SS("Focused ablations", "B"))
    story.append(B("A1: zero, one, or two Transformer encoders; quantifies the minimum useful global depth."))
    story.append(B("A2: 14 x 14 versus 28 x 28 token grids; tests accuracy against quadratic attention and latency."))
    story.append(B("A3: fixed equal fusion, concat-plus-projection, and adaptive channel gate."))
    story.append(B("A4: ordinary learned first convolution versus a fixed high/low-pass filter bank plus learned channels, motivated by MultiScaleCrackNet."))
    story.append(B("A5: scratch training versus ImageNet transfer for the standard ResNet-18 and, if weights are structurally compatible, a MobileViT reference."))
    story.append(P("Ablations are hierarchical: A1-A3 are required for the main claim; A4-A5 are secondary and should be omitted if compute is insufficient. This prevents an underpowered sweep from replacing the core controlled comparison."))
    story.append(SS("Parameter matching and fairness", "C"))
    story.append(P("Matching is performed on trainable parameter count, with MACs and latency reported rather than forced equal. The test set remains sealed while widths are adjusted. Every baseline receives an equal hyperparameter-search budget; the same settings need not be forced if that would systematically disadvantage one architecture. Search spaces and trial counts are published."))

    # VIII training
    story.append(S("Training Protocol", "VIII"))
    story.append(SS("Primary controlled training", "A"))
    story.append(P("Matched B1-B3 and H1 models are trained from scratch to isolate architecture. Use AdamW, initial learning rate 3e-4, weight decay 1e-2, batch 64 where memory permits, five warm-up epochs, cosine decay, and at most 100 epochs. Automatic mixed precision is allowed but must be identical across matched runs. Early stopping uses validation macro-F1 with patience 15 after a minimum 30 epochs; the checkpoint with the best validation macro-F1 is retained."))
    story.append(P("Three fixed seeds (42, 1337, 2026) control weight initialisation, sampling, and augmentation. Deterministic kernels are enabled where practical; any unavoidable non-determinism is reported. Gradient clipping at norm 1.0 prevents unstable Transformer updates. Batch size changes are compensated by gradient accumulation rather than by changing the effective batch."))
    story.append(SS("Loss and imbalance", "B"))
    story.append(P("The primary objective is weighted binary cross-entropy. The positive weight equals N_negative/N_positive computed from the training partition only. A balanced sampler is not combined with the weighted loss in the primary run because simultaneous correction can overcompensate; it is an optional loss ablation."))
    story.append(Eq("L = - w_pos y log(sigmoid(s)) - (1-y) log(1-sigmoid(s))", 6))
    story.append(SS("Hyperparameter selection", "C"))
    story.append(P("A small equal-budget search is allowed over learning rate {1e-3, 3e-4, 1e-4}, weight decay {1e-4, 1e-2, 5e-2}, and dropout {0.0, 0.1, 0.2}. Use successive narrowing rather than a full 27-cell grid: screen learning rate with fixed defaults, then weight decay, then dropout. Selection uses validation macro-F1 averaged across two provisional seeds; final reporting uses all three seeds. No test result may influence selection."))
    story.append(SS("Transfer-learning reference", "D"))
    story.append(P("For ResNet-18, replace the ImageNet classifier, train the new head for five epochs with the backbone frozen, then fine-tune all layers for up to 50 epochs at learning rate 1e-4. This model is a practical reference, not a matched causal baseline. If a pretrained MobileViT reference is included, use its official input normalisation and publish exactly which layers and checkpoints were loaded."))
    story.append(SS("Decision threshold", "E"))
    story.append(P("Report performance at the default probability threshold 0.5. A secondary operating point may be selected on validation data to maximise F1 or to achieve a predeclared minimum recall; label it clearly. The threshold is then frozen before any test prediction."))

    # IX Evaluation
    story.append(NextPageTemplate("OneCol"))
    story.append(PageBreak())
    story.append(S("Evaluation and Statistical Analysis", "IX"))
    story.append(SS("Predictive metrics", "A"))
    story.append(P("The primary metrics are crack-class recall, F1, PR-AUC, and balanced accuracy. Accuracy, precision, specificity, ROC-AUC, negative predictive value, confusion matrices, and per-surface metrics are also reported. PR-AUC receives equal prominence to ROC-AUC because cracks are the minority class."))
    metric_rows = [
        ["Metric", "Definition / reporting role"],
        ["Recall", "TP / (TP + FN); missed-crack sensitivity"],
        ["Precision", "TP / (TP + FP); reliability of crack alerts"],
        ["Specificity", "TN / (TN + FP); nuisance rejection"],
        ["F1", "2PR / (P + R); thresholded minority balance"],
        ["Balanced acc.", "0.5 x (recall + specificity)"],
        ["PR-AUC", "Threshold-free precision-recall quality under imbalance"],
        ["ROC-AUC", "Threshold-free rank discrimination"],
    ]
    story.append(Paragraph("TABLE IV. CORE PREDICTIVE METRICS", styles["TableCaption"]))
    story.append(table(metric_rows, [32 * mm, FULL_W - 32 * mm]))
    story.append(SS("Uncertainty and hypothesis tests", "B"))
    story.append(P("Point estimates alone are insufficient. Compute 95% percentile bootstrap confidence intervals with 10,000 resamples at the parent-photograph level. Tiles from a sampled parent enter together, preserving within-source dependence. For pairwise H1-versus-baseline differences, use the same bootstrap samples and report the confidence interval of the paired metric difference. A result is treated as supportive only when the interval excludes zero and the direction is consistent across seeds and held-out surfaces."))
    story.append(P("Do not apply an unclustered tile-level test as if 56,092 tiles were independent. If parent IDs cannot be recovered, statistical claims must be weakened, and leave-one-surface-out results become the principal evidence."))
    story.append(SS("Calibration", "C"))
    story.append(P("Report Brier score, reliability diagrams with ten equal-frequency bins, and expected calibration error as secondary outcomes. Temperature scaling may be fitted on validation logits and evaluated on test logits; both uncalibrated and calibrated results are retained."))
    story.append(SS("Efficiency", "D"))
    story.append(P("Report trainable parameters, model file size, MACs/FLOPs at 224 x 224, peak training and inference memory, and wall-clock latency. Measure batch-1 and batch-32 latency after 100 warm-up iterations over at least 1,000 timed inferences; report median and 95th percentile. Record processor/GPU, precision, framework, versions, threads, power mode, and input pipeline. The same preprocessing and synchronization rule applies to all models."))
    story.append(SS("Generalisation scorecard", "E"))
    story.append(P("For each held-out surface, report absolute metrics and the drop relative to pooled source-separated testing. Summarise mean and worst-surface F1/PR-AUC. A model that improves pooled accuracy but fails the worst surface does not satisfy the contribution claim."))

    story.append(S("Experimental Matrix and Data Flow", "X"))
    exp_rows = [
        ["ID", "Model / change", "Matched?", "Primary question answered"],
        ["B0", "ImageNet-pretrained ResNet-18", "No", "Practical transfer-learning reference"],
        ["B1", "Small CNN-only local branch", "Yes", "Are local features sufficient?"],
        ["B2", "Tiny raw-patch Transformer", "Yes", "Are global tokens sufficient?"],
        ["B3", "CNN stem -> Transformer, no local bypass", "Yes", "Does serial composition explain the gain?"],
        ["H1", "CrackFusion-Tiny, concat + 1 x 1 fusion", "Yes", "Does explicit local-global fusion help?"],
        ["A1", "H1 with 0/1/2 Transformer blocks", "Near", "Minimum useful attention depth"],
        ["A2", "H1 with 14 x 14 vs. 28 x 28 tokens", "No", "Accuracy-efficiency effect of token count"],
        ["A3", "Fixed, concat, adaptive gated fusion", "Near", "Does fusion mechanism matter?"],
        ["A4", "Learned vs. fixed-plus-learned edge filters", "Near", "Does a crack-edge prior help?"],
    ]
    story.append(Paragraph("TABLE V. MINIMUM CONTROLLED EXPERIMENT MATRIX", styles["TableCaption"]))
    story.append(table(exp_rows, [13 * mm, 70 * mm, 21 * mm, FULL_W - 104 * mm]))
    story.append(Spacer(1, 5 * mm))
    story.append(evaluation_figure())
    story.append(Paragraph("Fig. 3. Evaluation flow. Parent grouping is mandatory for the pooled claim; the held-out surface is never used for tuning.", styles["Caption"]))
    story.append(NextPageTemplate("TwoCol"))
    story.append(PageBreak())

    # XI Interpretability
    story.append(S("Interpretability and Error Analysis", "XI"))
    story.append(SS("Branch-specific explanations", "A"))
    story.append(PH(
        f"Generate Grad-CAM from the final local convolutional block to produce a class-discriminative local map "
        f"{cite('STKFXPT3')}. Generate attention rollout across the global branch to approximate information flow from "
        f"the final representation to input tokens {cite('VQRWTCHN')}. Upsample both maps to 224 x 224 with the same "
        "interpolation and overlay convention. The fused output is explained separately rather than presenting raw attention as proof of causal reasoning."))
    story.append(SS("Sampling plan", "B"))
    story.append(P("Create a fixed explanation panel with at least five examples per surface and outcome category: true positive, true negative, false positive, and false negative (up to 60 images if available). Selection is stratified by model confidence and frozen before visual comparison. Include shadows, joints, edges, stains, roughness, holes, and debris when present."))
    story.append(SS("Error taxonomy", "C"))
    for text in [
        "Missed thin/low-contrast crack; fragmented crack; large crack truncated by crop.",
        "Joint, seam, edge, or marking mistaken for a crack.",
        "Shadow, stain, debris, hole, or rough texture mistaken for a crack.",
        "Surface/domain failure specific to deck, wall, or pavement.",
        "Low-confidence or branch-disagreement case where local and global predictions differ.",
    ]:
        story.append(B(text))
    story.append(P("Two reviewers should independently label a subset of errors if feasible; disagreements are reconciled and the taxonomy counts are reported. Without segmentation ground truth, saliency maps remain qualitative. If an external mask dataset is introduced, localisation overlap must be reported separately from classification performance."))

    # XII Reproducibility
    story.append(S("Reproducibility, Reporting, and Governance", "XII"))
    story.append(SS("Required artifacts", "A"))
    repro = [
        ["Artifact", "Minimum content"],
        ["Data manifest", "Hashes, labels, surface, parent ID, split, exclusions"],
        ["Configuration", "Architecture dimensions, optimizer, schedule, augmentation, seed"],
        ["Environment", "OS, Python, framework/CUDA, hardware, dependency lock"],
        ["Training record", "Epoch metrics, selected checkpoint, early-stop reason, runtime"],
        ["Evaluation", "Per-seed predictions, thresholds, bootstrap code, confidence intervals"],
        ["Model card", "Intended use, prohibited use, data scope, known failure modes"],
    ]
    story.append(Paragraph("TABLE VI. REPRODUCIBILITY PACKAGE", styles["TableCaption"]))
    story.append(table(repro, [25 * mm, COL_W - 25 * mm]))
    story.append(SS("Reporting rules", "B"))
    story.append(B("Separate validation-selected results from the one-time test evaluation."))
    story.append(B("Report every planned model, including negative results; label exploratory experiments."))
    story.append(B("State the sample unit, parent grouping, class balance, and exact split counts."))
    story.append(B("Never compare headline accuracy across papers without noting dataset and protocol differences."))
    story.append(B("Distinguish measured values from targets or estimates; never present expected results as observations."))
    story.append(SS("Ethical and operational boundary", "C"))
    story.append(P("The classifier is a screening research prototype. It does not estimate crack width, depth, severity, propagation, or structural safety. False negatives can be consequential and predictions must not replace qualified inspection. Dataset licences, contributor attribution, and privacy/location metadata must be respected."))

    # XIII validity / risk
    story.append(S("Threats to Validity and Mitigation", "XIII"))
    threats = [
        ["Threat", "Mitigation"],
        ["Tile correlation / leakage", "Parent-group manifests; cluster bootstrap; no source overlap"],
        ["Class imbalance", "Weighted BCE; recall, F1, balanced accuracy, PR-AUC"],
        ["Surface/domain shift", "Three leave-one-surface-out evaluations; worst-surface score"],
        ["Hyperparameter bias", "Equal search budget; sealed test; publish all trials"],
        ["Compute confounding", "Parameter matching plus measured MACs, latency, memory"],
        ["Explanation overclaim", "Matched examples, error taxonomy, qualitative limitation"],
        ["Single-dataset scope", "Optional zero-tuning external stress test; bounded claims"],
        ["Unrecoverable parent IDs", "Do not claim source-separated pooling; prioritise domain-held-out evidence"],
    ]
    story.append(table(threats, [28 * mm, COL_W - 28 * mm]))
    story.append(SS("Success criteria", "A"))
    story.append(P("The hybrid hypothesis is supported only if H1 improves parent-cluster F1 and PR-AUC over both matched single-family baselines with paired 95% confidence intervals excluding zero, shows a consistent direction across all three held-out surfaces, and remains within the declared model/latency budget. An accuracy-only gain, a gain confined to one random split, or a gain obtained after test-driven tuning is insufficient."))
    story.append(P("If H1 fails, the study remains publishable as a careful negative result if the protocol is followed. The correct conclusion would be that a compact CNN is adequate under the tested constraints, not that attention is universally ineffective."))

    # XIV schedule
    story.append(S("Execution Plan", "XIV"))
    schedule = [
        ["Stage", "Work product", "Exit criterion"],
        ["1. Data audit", "Validated files and parent-level manifest", "No duplicates/corrupt files; split frozen"],
        ["2. Baselines", "B0-B3 trained and profiled", "Stable learning curves; equal search budget"],
        ["3. Hybrid", "H1 implementation and shape/parameter audit", "Within 1-3M target; deterministic forward pass"],
        ["4. Ablations", "A1-A3 required; A4-A5 if feasible", "Main mechanisms isolated"],
        ["5. Final tests", "Pooled and three surface-held-out results", "No post-test tuning"],
        ["6. Analysis", "Bootstrap CIs, efficiency, explanations, errors", "All claims traceable to artifacts"],
        ["7. Paper", "IEEE-style manuscript and repository", "Reproducibility checklist complete"],
    ]
    story.append(table(schedule, [20 * mm, 31 * mm, COL_W - 51 * mm]))
    story.append(P("A single student should prioritise Stages 1-5 and the required A1-A3 ablations. External data, fixed-filter A4, transfer A5, and calibration extensions are secondary. This ordering protects the core contribution from scope growth."))

    # XV conclusion and traceability share one full-width page.
    story.append(NextPageTemplate("OneCol"))
    story.append(PageBreak())
    story.append(S("Conclusion", "XV"))
    story.append(P("The proposed methodology converts the literature review into one testable, bounded study. CrackFusion-Tiny uses convolution where local bias is most valuable, attention only after spatial reduction, and one explicit fusion point that can be removed cleanly. The evidence standard is stronger than a conventional crop-random benchmark: parent-source separation, held-out surfaces, cluster-level uncertainty, balanced metrics, measured efficiency, and branch-specific explanations. These choices make the project feasible for one student while preserving a defensible research contribution."))

    # Appendix validation traceability
    story.append(S("Appendix A - Citation and Claim Traceability", "A"))
    trace_rows = [
        ["Refs.", "Validated role in this methodology", "Use boundary"],
        [cite('EHU23BPQ','2CJMWDZT'), "Field gaps: external validation, generalisation, deployment", "Not used to rank models"],
        [cite('UBGE2XUB'), "SDNET acquisition, counts, surfaces, nuisances, AlexNet benchmark", "Original paper does not establish a parent-group split"],
        [cite('9RL32V4L'), "Early patch-CNN data/training/F1", "Road patches; not directly comparable to SDNET"],
        [cite('B9X3LZ38'), "CCTNet architecture, datasets, training, in-domain/separate-bridge results", "No official code; split dependence noted"],
        [cite('WII7ZDKS'), "CSW-S tokens/attention/data/training/results", "Metric-formula/schedule inconsistencies not propagated"],
        [cite('KU57S9P4'), "Three-stream fixed-plus-learned CNN and all reported metrics", "Low SDNET recall retained; no cross-domain test"],
        [cite('RBFNPZW6'), "Duplicate/leakage evidence and cross-subset segmentation evaluation", "Segmentation metrics not treated as classification metrics"],
        [cite('GH8EIH8C','M9GHNUCF','P62GMGTN','CXTFQ3YB'), "Residual CNN, attention, ViT tokens, small-data training", "Large-scale headline results are not project targets"],
        [cite('GTCI5SK8','LQT8CXBK','GWUJX2DK','2KCLWMMZ','AGUTHS2H'), "Hierarchy, convolutional tokens, coupling, staged/local-global hybrids", "Complex modules simplified to preserve ablatability"],
        [cite('UZT7VV56','F38CEX55','4YLNLIG8','8XFL6FCR','HKLMLZIF'), "Mobile/lightweight fusion, latency, memory, multi-level interaction", "Device-specific speed claims not transferred"],
        [cite('STKFXPT3','VQRWTCHN'), "Original Grad-CAM and attention rollout/flow methods", "Explanations described as post hoc, not causal proof"],
    ]
    story.append(table(trace_rows, [20 * mm, 87 * mm, FULL_W - 107 * mm]))
    story.append(Spacer(1, 5 * mm))
    story.append(PH(
        "<b>Validation statement.</b> All 24 bibliography records were checked against the editable Zotero project "
        "library on 30 August 2026. The methodology uses 22 previously reviewed records plus two primary "
        "interpretability papers added during Phase 3. No result in this document is presented as a newly observed "
        "experimental result.", "Callout"))

    # References
    story.append(NextPageTemplate("TwoCol"))
    story.append(PageBreak())
    story.append(S("References", "R"))
    by_key = {item["key"]: item for item in items}
    for key in ORDER:
        story.append(Paragraph(reference_text(by_key[key], REFNO[key]), styles["Ref"]))
    return story


def main():
    if not ITEMS_JSON.exists():
        raise FileNotFoundError(f"Missing Zotero metadata snapshot: {ITEMS_JSON}")
    items = json.loads(ITEMS_JSON.read_text(encoding="utf-8"))
    keys = {item["key"] for item in items}
    missing = [key for key in ORDER if key not in keys]
    if missing:
        raise ValueError(f"Missing bibliography records: {missing}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = MethodologyDoc(str(OUT))
    doc.build(build_story(items))
    print(OUT)


if __name__ == "__main__":
    main()

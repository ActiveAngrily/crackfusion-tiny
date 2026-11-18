"""CrackFusion-Tiny Streamlit Research & Screening Web Application."""

from __future__ import annotations

import sys
from pathlib import Path
from PIL import Image
import streamlit as st

# Add current directory to path so core_model imports cleanly
WEBAPP_DIR = Path(__file__).resolve().parent
if str(WEBAPP_DIR) not in sys.path:
    sys.path.insert(0, str(WEBAPP_DIR))

from core_model import (
    CrackFusionTiny,
    count_parameters,
    find_available_checkpoints,
    generate_sample_tile,
    load_model,
    predict_and_explain,
)

st.set_page_config(
    page_title="CrackFusion-Tiny | Concrete Crack Inspection",
    page_icon="🧱",
    layout="wide",
)

# --- Checkpoint & Model Caching ---
@st.cache_resource(show_spinner="Loading CrackFusion-Tiny model...")
def get_cached_model(ckpt_path: str | None):
    return load_model(ckpt_path, device="cpu")


# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Model Configuration")
    
    available_ckpts = find_available_checkpoints()
    ckpt_options = [str(p) for p in available_ckpts]
    
    if ckpt_options:
        # Default to best_seed_2026.pt if available
        default_idx = 0
        for i, opt in enumerate(ckpt_options):
            if "2026" in opt:
                default_idx = i
                break
        
        selected_ckpt = st.selectbox(
            "Select Checkpoint",
            options=ckpt_options,
            index=default_idx,
            format_func=lambda x: Path(x).name,
            help="Trained model weights (.pt files).",
        )
    else:
        st.warning("No `.pt` file found in `webapp/checkpoints/`. Using demo initialization.")
        selected_ckpt = None

    bundle = get_cached_model(selected_ckpt)

    threshold = st.slider(
        "Decision Threshold",
        min_value=0.05,
        max_value=0.95,
        value=float(bundle["threshold"]),
        step=0.05,
        help="Probabilities greater than or equal to this threshold are classified as Crack.",
    )

    st.markdown("---")
    st.subheader("Model Specs")
    st.markdown(
        f"- **Architecture:** `CrackFusionTiny-v1`\n"
        f"- **Parameters:** `{count_parameters(bundle['model']):,}`\n"
        f"- **Input Shape:** `3 × 224 × 224`\n"
        f"- **Seed:** `{bundle['seed']}`\n"
        f"- **Status:** {'🟢 Trained Checkpoint' if bundle['is_trained'] else '🟡 Demo Fallback'}"
    )
    if bundle.get("epoch"):
        st.markdown(f"- **Trained Epoch:** `{bundle['epoch']}`")

    st.markdown("---")
    st.caption("CrackFusion-Tiny • SDNET2018 Concrete Benchmark")


# --- Main Application Header ---
st.title("🧱 CrackFusion-Tiny: Concrete Crack Inspection")
st.markdown(
    "A compact, parallel **CNN–Transformer hybrid model** ($284,337$ parameters) for automated concrete crack screening. "
    "Upload a concrete surface photo or run an instant sample tile below."
)

st.markdown("---")

# --- Input Section ---
col_upload, col_sample = st.columns([3, 2])

with col_upload:
    uploaded_file = st.file_uploader(
        "Upload a concrete surface photo / tile (JPG, JPEG, PNG)",
        type=["jpg", "jpeg", "png"],
    )

with col_sample:
    st.write("**Or try an instant sample tile:**")
    btn_col1, btn_col2 = st.columns(2)
    sample_cracked = btn_col1.button("🧱 Sample Cracked Tile", use_container_width=True)
    sample_intact = btn_col2.button("🟩 Sample Intact Tile", use_container_width=True)

# Determine active image
active_image: Image.Image | None = None
image_source_label = ""

if uploaded_file is not None:
    active_image = Image.open(uploaded_file).convert("RGB")
    image_source_label = f"Uploaded: {uploaded_file.name}"
elif sample_cracked:
    active_image = generate_sample_tile("cracked")
    image_source_label = "Built-in Sample: Cracked Concrete Tile"
elif sample_intact:
    active_image = generate_sample_tile("intact")
    image_source_label = "Built-in Sample: Intact (Non-cracked) Tile"

# --- Inference & Results Section ---
if active_image is not None:
    with st.spinner("Running inference and generating Grad-CAM heatmap..."):
        result = predict_and_explain(bundle, active_image, threshold=threshold)

    prob = result["probability"]
    is_crack = result["is_crack"]
    prob_percent = prob * 100.0

    st.markdown(f"#### Results for: *{image_source_label}*")

    # Big Banner Metric
    if is_crack:
        st.error(
            f"### 🚨 CRACK DETECTED\n\n"
            f"**Confidence:** `{prob_percent:.2f}%` (Threshold: `{threshold:.2f}`, Raw Logit: `{result['logit']:+.3f}`)"
        )
    else:
        st.success(
            f"### ✅ NO CRACK DETECTED (INTACT)\n\n"
            f"**Confidence:** `{100.0 - prob_percent:.2f}% non-crack` (Crack Probability: `{prob_percent:.2f}%`, Threshold: `{threshold:.2f}`)"
        )

    # Progress bar for probability
    st.progress(min(max(prob, 0.0), 1.0))

    # Side-by-side Images
    img_col1, img_col2 = st.columns(2)

    with img_col1:
        st.subheader("📷 Input Image")
        st.image(
            result["crop_image"],
            caption="224 × 224 Center Crop (Model Input)",
            use_container_width=True,
        )

    with img_col2:
        st.subheader("🔥 Model Attention (Grad-CAM)")
        st.image(
            result["overlay_image"],
            caption="Grad-CAM Activation Map (Where the model focused)",
            use_container_width=True,
        )

    # Technical Details Expander
    with st.expander("🔍 View Technical Diagnostics & Raw Values"):
        d_col1, d_col2, d_col3, d_col4 = st.columns(4)
        d_col1.metric("Predicted Class", "Crack" if is_crack else "Non-Crack")
        d_col2.metric("Sigmoid Score P(y=1)", f"{prob:.4f}")
        d_col3.metric("Raw Logit", f"{result['logit']:+.4f}")
        d_col4.metric("Active Threshold", f"{threshold:.2f}")

        st.json({
            "checkpoint_loaded": bundle.get("label"),
            "architecture": "CrackFusionTiny-v1",
            "trainable_parameters": 284337,
            "normalization_mean": bundle["mean"],
            "normalization_std": bundle["std"],
            "seed": bundle.get("seed"),
            "epoch": bundle.get("epoch"),
        })

else:
    st.info("👆 Upload an image or click one of the sample buttons to inspect concrete surface integrity.")

"""Quick test script to verify CrackFusion-Tiny model and Grad-CAM explainability."""

from __future__ import annotations

import sys
from pathlib import Path

WEBAPP_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(WEBAPP_DIR))

from core_model import (
    CrackFusionTiny,
    count_parameters,
    find_available_checkpoints,
    generate_sample_tile,
    load_model,
    predict_and_explain,
)


def test_webapp_core():
    print("1. Checking available checkpoints...")
    ckpts = find_available_checkpoints()
    print(f"   Found {len(ckpts)} checkpoint(s): {[c.name for c in ckpts]}")

    print("2. Loading CrackFusionTiny model...")
    bundle = load_model()
    print(f"   Loaded: {bundle['label']}")
    print(f"   Is trained: {bundle['is_trained']}")
    param_count = count_parameters(bundle["model"])
    print(f"   Parameter count: {param_count}")
    assert param_count == 284337, f"Expected 284,337 parameters, got {param_count}"

    print("3. Generating synthetic test tile (cracked)...")
    img_cracked = generate_sample_tile("cracked")
    res_cracked = predict_and_explain(bundle, img_cracked)
    print(f"   Cracked Sample -> Prob: {res_cracked['probability']:.4f}, Prediction: {res_cracked['is_crack']}")
    assert 0.0 <= res_cracked["probability"] <= 1.0
    assert res_cracked["overlay_image"].size == (224, 224)

    print("4. Generating synthetic test tile (intact)...")
    img_intact = generate_sample_tile("intact")
    res_intact = predict_and_explain(bundle, img_intact)
    print(f"   Intact Sample -> Prob: {res_intact['probability']:.4f}, Prediction: {res_intact['is_crack']}")
    assert 0.0 <= res_intact["probability"] <= 1.0
    assert res_intact["overlay_image"].size == (224, 224)

    print("\nALL SIMPLE WEBAPP VERIFICATION CHECKS PASSED!")


if __name__ == "__main__":
    test_webapp_core()

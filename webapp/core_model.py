"""CrackFusion-Tiny core model architecture, loader, and Grad-CAM explainability."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional
import numpy as np
from PIL import Image, ImageDraw
import torch
from torch import nn
import torch.nn.functional as F
from torchvision import transforms as T
import matplotlib as mpl


class ConvBNGELU(nn.Sequential):
    """3x3 or 1x1 Convolution + BatchNorm2d + GELU."""

    def __init__(self, cin: int, cout: int, kernel: int = 3, stride: int = 1):
        super().__init__(
            nn.Conv2d(cin, cout, kernel, stride, kernel // 2, bias=False),
            nn.BatchNorm2d(cout),
            nn.GELU(),
        )


class DSResidual(nn.Module):
    """Depthwise-separable residual block."""

    def __init__(self, cin: int, cout: int, stride: int = 1):
        super().__init__()
        self.body = nn.Sequential(
            nn.Conv2d(cin, cin, 3, stride, 1, groups=cin, bias=False),
            nn.BatchNorm2d(cin),
            nn.GELU(),
            nn.Conv2d(cin, cout, 1, bias=False),
            nn.BatchNorm2d(cout),
        )
        self.skip = (
            nn.Identity()
            if cin == cout and stride == 1
            else nn.Sequential(
                nn.Conv2d(cin, cout, 1, stride, bias=False),
                nn.BatchNorm2d(cout),
            )
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return F.gelu(self.body(x) + self.skip(x))


class CrackFusionTiny(nn.Module):
    """Parallel local/global classifier for 224x224 RGB images (exact 284,337 parameters)."""

    def __init__(self):
        super().__init__()
        self.stem = nn.Sequential(
            ConvBNGELU(3, 32, stride=2),
            DSResidual(32, 48, 2),
            DSResidual(48, 64, 2),
        )
        self.local = nn.Sequential(
            DSResidual(64, 96),
            DSResidual(96, 96),
            nn.AvgPool2d(2),
        )
        self.tokenizer = ConvBNGELU(64, 96, stride=2)
        self.position = nn.Parameter(torch.empty(1, 96, 14, 14))
        nn.init.trunc_normal_(self.position, std=0.02)
        self.encoders = nn.ModuleList(
            [
                nn.TransformerEncoderLayer(
                    96,
                    4,
                    dim_feedforward=192,
                    dropout=0.1,
                    activation="gelu",
                    batch_first=True,
                    norm_first=True,
                )
                for _ in range(2)
            ]
        )
        self.token_norm = nn.LayerNorm(96)
        self.fusion = ConvBNGELU(192, 128, kernel=1)
        self.head = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Dropout(0.2),
            nn.Linear(128, 1),
        )

    def forward(self, x: torch.Tensor, return_features: bool = False):
        if x.ndim != 4 or tuple(x.shape[1:]) != (3, 224, 224) or x.shape[0] == 0:
            raise ValueError("Expected nonempty floating-point input [B, 3, 224, 224]")
        if not x.is_floating_point():
            raise TypeError("Preprocess pixels into a floating-point tensor first")

        shared = self.stem(x)
        local = self.local(shared)
        token_map = self.tokenizer(shared)
        tokens = (token_map + self.position).flatten(2).transpose(1, 2)
        for encoder in self.encoders:
            tokens = encoder(tokens)
        tokens = self.token_norm(tokens)
        global_map = tokens.transpose(1, 2).reshape(x.shape[0], 96, 14, 14)
        fused = self.fusion(torch.cat((local, global_map), dim=1))
        logits = self.head(fused)

        if return_features:
            return logits, {
                "stem": shared,
                "local": local,
                "tokens": tokens,
                "global_map": global_map,
                "fused": fused,
            }
        return logits


def count_parameters(model: nn.Module) -> int:
    """Returns the total number of trainable parameters."""
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def make_eval_transform(mean: List[float], std: List[float]) -> T.Compose:
    """Exact deterministic preprocessing matching training pipeline."""
    return T.Compose([
        T.Resize(256),
        T.CenterCrop(224),
        T.ToTensor(),
        T.Normalize(mean, std),
    ])


def find_available_checkpoints(search_dirs: Optional[List[Path]] = None) -> List[Path]:
    """Finds all unique valid .pt checkpoints in expected locations."""
    if search_dirs is None:
        base_dir = Path(__file__).resolve().parent
        search_dirs = [
            base_dir / "checkpoints",
            base_dir.parent / "checkpoints",
            base_dir.parent / "outputs",
        ]
    found = []
    seen_names = set()
    for d in search_dirs:
        if d.is_dir():
            for p in sorted(d.rglob("*.pt")):
                if not p.name.startswith("last_") and p.name not in seen_names:
                    seen_names.add(p.name)
                    found.append(p)
    return found


def load_model(
    checkpoint_path: Optional[str | Path] = None,
    device: str = "cpu",
) -> Dict[str, Any]:
    """Loads a verified CrackFusionTiny model with weights, transforms, and metadata."""
    model = CrackFusionTiny().to(device).eval()
    assert count_parameters(model) == 284337, "Parameter count mismatch"

    target_path = Path(checkpoint_path) if checkpoint_path else None
    if target_path is None or not target_path.is_file():
        candidates = find_available_checkpoints()
        if not candidates:
            # Auto-download best_seed_2026.pt on cloud deployment if missing
            try:
                import urllib.request
                default_ckpt_dir = Path(__file__).resolve().parent / "checkpoints"
                default_ckpt_dir.mkdir(parents=True, exist_ok=True)
                download_target = default_ckpt_dir / "best_seed_2026.pt"
                url = "https://drive.usercontent.google.com/download?id=1LY5RbWp4gPbHBBDamXJA0oaVFF3n-Oih&export=download"
                urllib.request.urlretrieve(url, download_target)
                if download_target.is_file():
                    candidates = [download_target]
            except Exception:
                pass

        # Prefer best_seed_2026.pt if available
        best_2026 = [c for c in candidates if "2026" in c.name]
        if best_2026:
            target_path = best_2026[0]
        elif candidates:
            target_path = candidates[0]

    if target_path and target_path.is_file():
        ckpt = torch.load(target_path, map_location=device, weights_only=True)
        model.load_state_dict(ckpt["model"])
        mean = list(ckpt.get("mean", [0.5412, 0.5348, 0.5219]))
        std = list(ckpt.get("std", [0.1842, 0.1815, 0.1796]))
        threshold = float(ckpt.get("threshold", 0.5))
        seed = ckpt.get("seed", 2026)
        epoch = ckpt.get("epoch", None)
        val_metrics = ckpt.get("validation_metrics", {})
        is_trained = True
        label = f"{target_path.name} (Seed {seed}, Epoch {epoch})"
    else:
        # Fallback deterministic weights
        torch.manual_seed(42)
        mean = [0.5412, 0.5348, 0.5219]
        std = [0.1842, 0.1815, 0.1796]
        threshold = 0.5
        seed = 42
        epoch = 0
        val_metrics = {}
        is_trained = False
        label = "Untrained Demo Fallback (seed=42)"

    return {
        "model": model,
        "transform": make_eval_transform(mean, std),
        "mean": mean,
        "std": std,
        "threshold": threshold,
        "seed": seed,
        "epoch": epoch,
        "validation_metrics": val_metrics,
        "is_trained": is_trained,
        "checkpoint_path": str(target_path) if target_path else None,
        "label": label,
    }


def predict_and_explain(
    bundle: Dict[str, Any],
    pil_image: Image.Image,
    threshold: Optional[float] = None,
    device: str = "cpu",
) -> Dict[str, Any]:
    """Runs CrackFusion-Tiny inference and computes Local CNN Grad-CAM."""
    model: CrackFusionTiny = bundle["model"]
    model.eval()

    if threshold is None:
        threshold = bundle["threshold"]

    rgb = pil_image.convert("RGB")
    crop_transform = T.Compose([T.Resize(256), T.CenterCrop(224)])
    crop_224 = crop_transform(rgb)

    x = bundle["transform"](rgb).unsqueeze(0).to(device)
    x.requires_grad_(True)

    # Forward pass up to the local branch layer
    shared = model.stem(x)
    local_conv = model.local[:2](shared)  # shape [1, 96, 28, 28]
    local_conv.retain_grad()
    local = model.local[2](local_conv)    # shape [1, 96, 14, 14]

    token_map = model.tokenizer(shared)
    tokens = (token_map + model.position).flatten(2).transpose(1, 2)
    for encoder in model.encoders:
        tokens = encoder(tokens)
    tokens = model.token_norm(tokens)
    global_map = tokens.transpose(1, 2).reshape(x.shape[0], 96, 14, 14)

    fused = model.fusion(torch.cat((local, global_map), dim=1))
    logits = model.head(fused)

    # Backprop for Grad-CAM
    model.zero_grad(set_to_none=True)
    logits[0, 0].backward()

    # Compute Grad-CAM weights over the 28x28 local feature map
    alpha = local_conv.grad.mean(dim=(2, 3), keepdim=True)
    cam_raw = F.relu((alpha * local_conv.detach()).sum(dim=1, keepdim=True))
    cam_upsampled = F.interpolate(cam_raw, size=(224, 224), mode="bilinear", align_corners=False)
    cam_np = cam_upsampled.squeeze().cpu().numpy()

    # Normalize heatmap into [0.0, 1.0]
    vmin, vmax = float(cam_np.min()), float(cam_np.max())
    if vmax - vmin > 1e-8:
        cam_norm = (cam_np - vmin) / (vmax - vmin)
    else:
        cam_norm = np.zeros((224, 224), dtype=np.float32)

    # Build RGB overlay using 'inferno' colormap
    colormap = mpl.colormaps["inferno"]
    heatmap_colored = colormap(cam_norm)[:, :, :3]  # [224, 224, 3] in [0, 1]
    crop_np = np.array(crop_224, dtype=np.float32) / 255.0
    overlay_np = np.clip(0.55 * crop_np + 0.45 * heatmap_colored, 0.0, 1.0)
    overlay_img = Image.fromarray((overlay_np * 255).astype(np.uint8))

    prob = float(logits.detach().sigmoid().item())
    is_crack = prob >= threshold

    return {
        "probability": prob,
        "is_crack": is_crack,
        "logit": float(logits.detach().item()),
        "threshold": threshold,
        "crop_image": crop_224,
        "overlay_image": overlay_img,
        "heatmap": cam_norm,
    }


def generate_sample_tile(kind: str = "cracked") -> Image.Image:
    """Generates a synthetic 256x256 concrete tile for zero-setup demo testing."""
    rng = np.random.default_rng(101 if kind == "cracked" else 202)
    base = rng.normal(loc=145, scale=14, size=(256, 256, 3)).clip(0, 255).astype(np.uint8)
    img = Image.fromarray(base, mode="RGB")
    if kind == "cracked":
        draw = ImageDraw.Draw(img)
        pts = [(30, 24), (74, 68), (110, 115), (140, 160), (182, 204), (225, 235)]
        draw.line(pts, fill=(35, 30, 28), width=4)
        draw.line([(74, 68), (95, 75)], fill=(45, 40, 38), width=2)
    return img

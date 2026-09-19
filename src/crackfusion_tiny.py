"""CrackFusion-Tiny model architecture."""

import torch
from torch import nn
import torch.nn.functional as F


class ConvBNGELU(nn.Sequential):
    def __init__(self, cin: int, cout: int, kernel: int = 3, stride: int = 1):
        super().__init__(
            nn.Conv2d(cin, cout, kernel, stride, kernel // 2, bias=False),
            nn.BatchNorm2d(cout),
            nn.GELU(),
        )


class DSResidual(nn.Module):
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
    """Parallel local/global classifier for 224×224 RGB images."""

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
    return sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)


def _smoke_test() -> None:
    model = CrackFusionTiny()
    inputs = torch.randn(2, 3, 224, 224)
    logits, features = model(inputs, return_features=True)
    assert logits.shape == (2, 1)
    assert features["local"].shape == (2, 96, 14, 14)
    assert features["tokens"].shape == (2, 196, 96)
    assert count_parameters(model) == 284_337
    logits.sum().backward()
    assert all(parameter.grad is not None for parameter in model.parameters())
    print({"parameters": count_parameters(model), "output": list(logits.shape)})


if __name__ == "__main__":
    _smoke_test()

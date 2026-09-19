"""Build the self-contained implementation notebook; run from any directory."""
from pathlib import Path
import nbformat as nbf

cells = []


def md(source):
    cells.append(nbf.v4.new_markdown_cell(source.strip()))


def code(source):
    cells.append(nbf.v4.new_code_cell(source.strip()))


md(r"""
# CrackFusion-Tiny: implementation, validation, and training

This is the project's **custom model**, trained from scratch. Run all cells in order.
The default run needs no dataset: it checks the architecture, gradients, checkpoint
round trip, batch independence, and learning on an artificial stripe task. Those
checks establish software behavior, **not concrete-crack accuracy**.

For SDNET2018, edit the configuration cell and enable `RUN_TRAINING`. Enable
`RUN_TEST` only after validation choices are frozen. No data is downloaded silently.
The existing MobileViT notebooks remain separate transfer-learning references.

## 1. Research and implementation decisions

The local Phase 2 synthesis and Phase 3 methodology prescribe this architecture.
The following primary sources motivate its ingredients, not its unmeasured accuracy:

| Source | What we use | What we do not claim to reproduce |
|---|---|---|
| [MobileViT, Mehta & Rastegari](https://arxiv.org/abs/2110.02178) | convolutional features plus compact global processing | MobileViT's patch unfolding scheme or pretrained weights |
| [CvT, Wu et al.](https://arxiv.org/abs/2103.15808) | overlapping convolutional token formation | CvT's full hierarchy and convolutional Q/K/V projections |
| [Conformer, Peng et al.](https://arxiv.org/abs/2105.03889) | identifiable local/global paths | repeated bidirectional coupling |
| [ResNet, He et al.](https://arxiv.org/abs/1512.03385) | residual shortcuts | a ResNet backbone |
| [PyTorch TransformerEncoder](https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoder.html) | standard encoder layers | cloned identical initial weights: we instantiate layers separately |

The architecture uses 224×224 RGB input, depthwise residual downsampling, two
96-dimensional, four-head, pre-norm GELU Transformer blocks (MLP width 192), a
learned 14×14 positional grid, and one concat/1×1 fusion. Stochastic depth is 0,
within the methodology's ≤0.1 limit; attention/residual dropout is 0.1 and head
dropout is 0.2. A final LayerNorm stabilizes the pre-norm encoder output.

**Parameter-budget correction:** the prescribed widths produce substantially fewer
than the preliminary 1–3M estimate. The actual count below is authoritative; no
padding layers are added to meet that estimate. Baselines must match this measured
count. This is a documented reconciliation of the methodology, not a 1–3M variant.

## 2. Environment

In a fresh Colab runtime, run the commented installation line if imports fail.
The notebook prints exact versions for each execution. Select a GPU for full training.
""")
code(r"""
# %pip install torch torchvision numpy pillow scikit-learn matplotlib
import csv, hashlib, io, json, math, random, statistics, time
from pathlib import Path
from tempfile import TemporaryDirectory
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
import torchvision
from torchvision import transforms as T
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, confusion_matrix,
    f1_score, precision_score, recall_score, roc_auc_score, average_precision_score)

def seed_everything(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True

DEVICE = torch.device('cuda' if torch.cuda.is_available() else
                      'mps' if torch.backends.mps.is_available() else 'cpu')
torch.set_num_threads(min(4, torch.get_num_threads()))
seed_everything(42)
print({'torch': str(torch.__version__), 'torchvision': str(torchvision.__version__),
       'device': str(DEVICE), 'cpu_threads': torch.get_num_threads()})
""")
md("""
## 3. Complete model

All shapes use PyTorch's batch/channel/height/width order. The two branches receive
the **same** stem output. Tokens return to their original spatial ordering before
fusion. `return_features=True` exposes branch tensors for inspection or attribution.
The model returns a raw logit; sigmoid belongs in inference, not before BCE loss.
Input resolution is deliberately fixed and checked rather than silently reshaped.
""")
code(r"""
class ConvBNGELU(nn.Sequential):
    def __init__(self, cin, cout, kernel=3, stride=1):
        super().__init__(nn.Conv2d(cin, cout, kernel, stride, kernel // 2, bias=False),
                         nn.BatchNorm2d(cout), nn.GELU())

class DSResidual(nn.Module):
    def __init__(self, cin, cout, stride=1):
        super().__init__()
        self.body = nn.Sequential(
            nn.Conv2d(cin, cin, 3, stride, 1, groups=cin, bias=False),
            nn.BatchNorm2d(cin), nn.GELU(),
            nn.Conv2d(cin, cout, 1, bias=False), nn.BatchNorm2d(cout))
        self.skip = nn.Identity() if cin == cout and stride == 1 else nn.Sequential(
            nn.Conv2d(cin, cout, 1, stride, bias=False), nn.BatchNorm2d(cout))
        self.activation = nn.GELU()

    def forward(self, x):
        return self.activation(self.body(x) + self.skip(x))

class CrackFusionTiny(nn.Module):
    def __init__(self):
        super().__init__()
        self.stem = nn.Sequential(ConvBNGELU(3, 32, stride=2),
                                 DSResidual(32, 48, 2), DSResidual(48, 64, 2))
        self.local = nn.Sequential(DSResidual(64, 96), DSResidual(96, 96),
                                   nn.AvgPool2d(2))
        self.tokenizer = ConvBNGELU(64, 96, stride=2)
        self.position = nn.Parameter(torch.empty(1, 96, 14, 14))
        nn.init.trunc_normal_(self.position, std=0.02)
        # Independently constructed layers have independent initial random weights.
        self.encoders = nn.ModuleList([
            nn.TransformerEncoderLayer(96, 4, dim_feedforward=192, dropout=0.1,
                activation='gelu', batch_first=True, norm_first=True)
            for _ in range(2)])
        self.token_norm = nn.LayerNorm(96)
        self.fusion = ConvBNGELU(192, 128, kernel=1)
        self.head = nn.Sequential(nn.AdaptiveAvgPool2d(1), nn.Flatten(),
                                  nn.Dropout(0.2), nn.Linear(128, 1))

    def forward(self, x, return_features=False):
        if x.ndim != 4 or tuple(x.shape[1:]) != (3, 224, 224) or x.shape[0] == 0:
            raise ValueError('Expected nonempty floating-point input [B, 3, 224, 224]')
        if not x.is_floating_point():
            raise TypeError('Preprocess pixels into a floating-point tensor first')
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
            return logits, dict(stem=shared, local=local, tokens=tokens,
                                global_map=global_map, fused=fused)
        return logits

model = CrackFusionTiny()
PARAMETERS = sum(p.numel() for p in model.parameters())
print(f'Trainable parameters: {PARAMETERS:,} ({PARAMETERS / 1e6:.3f}M)')
print(f'Parameter storage in float32: {PARAMETERS * 4 / 1024**2:.2f} MiB')
with torch.no_grad():
    logits, features = model.eval()(torch.randn(2, 3, 224, 224), return_features=True)
print({name: list(value.shape) for name, value in features.items()})
print('logits:', list(logits.shape))
""")
md("""
## 4. Executable architecture and optimization checks

These checks run on CPU for repeatability and then test a forward/backward pass on
the selected device. They verify both branches receive gradients, a saved model
reproduces predictions, evaluation does not mix samples, and bad inputs fail clearly.
""")
code(r"""
def validate_model():
    seed_everything(42)
    net = CrackFusionTiny()
    x = torch.randn(2, 3, 224, 224)
    y = torch.tensor([[0.], [1.]])
    scores, maps = net(x, return_features=True)
    expected = {'stem': (2, 64, 28, 28), 'local': (2, 96, 14, 14),
                'tokens': (2, 196, 96), 'global_map': (2, 96, 14, 14),
                'fused': (2, 128, 14, 14)}
    assert scores.shape == (2, 1)
    assert all(tuple(maps[k].shape) == v for k, v in expected.items())
    loss = nn.BCEWithLogitsLoss()(scores, y)
    loss.backward()
    assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in net.parameters())
    for module in (net.stem, net.local, net.tokenizer, net.encoders, net.fusion, net.head):
        assert sum(p.grad.abs().sum().item() for p in module.parameters()) > 0
    assert net.position.grad.abs().sum() > 0
    assert not torch.equal(net.encoders[0].self_attn.in_proj_weight,
                           net.encoders[1].self_attn.in_proj_weight)
    net.eval()
    with torch.no_grad():
        reference = net(x)
        torch.testing.assert_close(net(x[:1]), reference[:1], rtol=1e-4, atol=1e-5)
        torch.testing.assert_close(net(x), reference)
    buffer = io.BytesIO()
    torch.save(net.state_dict(), buffer)
    buffer.seek(0)
    restored = CrackFusionTiny().eval()
    restored.load_state_dict(torch.load(buffer, weights_only=True))
    with torch.no_grad():
        torch.testing.assert_close(restored(x), reference)
    for bad in (torch.randn(2, 3, 256, 256), torch.randn(2, 1, 224, 224),
                torch.empty(0, 3, 224, 224)):
        try:
            net(bad)
        except ValueError:
            pass
        else:
            raise AssertionError('Bad shape accepted')
    device_net = CrackFusionTiny().to(DEVICE).train()
    device_loss = nn.BCEWithLogitsLoss()(device_net(x.to(DEVICE)), y.to(DEVICE))
    device_loss.backward()
    assert torch.isfinite(device_loss)
    assert all(p.grad is not None and torch.isfinite(p.grad).all()
               for p in device_net.parameters())
    return {'shape_checks': 'passed', 'all_parameter_gradients': 'passed',
            'checkpoint_round_trip': 'passed', 'batch_independence': 'passed',
            'input_validation': 'passed', 'device_backward': str(DEVICE)}

validation_report = validate_model()
print(json.dumps(validation_report, indent=2))
""")
md("""
## 5. Can it learn? Artificial stripe overfit check

Eight synthetic textured images, half with a dark vertical stripe, are deliberately
reused for optimization and measurement. This checks that training can reduce loss;
it is neither a held-out test nor evidence of crack generalization. The trained
toy model is discarded before any real-data training.
""")
code(r"""
seed_everything(42)
toy_x = (0.6 + 0.08 * torch.randn(8, 3, 224, 224)).clamp(0, 1)
toy_y = torch.tensor([0, 1] * 4, dtype=torch.float32).view(-1, 1)
for i in range(1, 8, 2):
    toy_x[i, :, :, 105:113] = 0.05
toy_model = CrackFusionTiny().train()
toy_optimizer = torch.optim.AdamW(toy_model.parameters(), lr=1e-3)
toy_loss_fn = nn.BCEWithLogitsLoss()
toy_losses = []
for step in range(50):
    toy_optimizer.zero_grad(set_to_none=True)
    toy_loss = toy_loss_fn(toy_model(toy_x), toy_y)
    assert torch.isfinite(toy_loss)
    toy_loss.backward()
    nn.utils.clip_grad_norm_(toy_model.parameters(), 1.0)
    toy_optimizer.step()
    toy_losses.append(toy_loss.item())
toy_model.eval()
with torch.no_grad():
    toy_logits = toy_model(toy_x)
    toy_accuracy = ((toy_logits >= 0) == toy_y.bool()).float().mean().item()
assert np.mean(toy_losses[-5:]) < 0.5 * np.mean(toy_losses[:5])
assert toy_accuracy >= 0.875
validation_report['toy_first_loss'] = toy_losses[0]
validation_report['toy_last_loss'] = toy_losses[-1]
validation_report['toy_training_accuracy'] = toy_accuracy
print({k: v for k, v in validation_report.items() if k.startswith('toy')})
plt.plot(toy_losses)
plt.xlabel('Optimization step'); plt.ylabel('BCE loss')
plt.title('Artificial stripe memorization — software check only'); plt.show()
del toy_model, toy_optimizer
""")
md("""
## 6. Real-data configuration

Obtain [SDNET2018 from its official record](https://digitalcommons.usu.edu/all_datasets/48/).
Use the existing audit notebook to inventory it. Supply a CSV with columns
`path,label,surface,parent_id,split`; paths are relative to `DATA_ROOT`, labels are
0=no crack and 1=crack, and splits are `train`, `validation`, `test`.

`PROTOCOL='source_separated'` requires real parent IDs with no parent crossing
partitions. Document how those IDs were obtained in `PARENT_ID_PROVENANCE`; this
code cannot establish that a supplied ID is historically correct. Never manufacture
one ID per tile. `PROTOCOL='development'` allows the existing tile split, but forbids
test reporting. Exact file duplicates across splits are rejected in either mode.
Full near-duplicate auditing and parent verification remain dataset curation work.

Training uses all layers from the start: the MobileViT frozen-head warm-up does not
apply to random weights. Normalization is estimated from training images only.
Batch accumulation maintains an effective batch of 64 (except the final short group).
""")
code(r"""
DATA_ROOT = Path('/content/SDNET2018')
MANIFEST = Path('/content/manifest.csv')
OUTPUT_ROOT = Path('output/crackfusion_tiny')
PROTOCOL = 'source_separated'  # or 'development'; never relabel tile results
PARENT_ID_PROVENANCE = ''      # describe the verified mapping's source
RUN_TRAINING = False
RUN_TEST = False
SEEDS = (42, 1337, 2026)
BATCH_SIZE = 16
EFFECTIVE_BATCH = 64
MAX_EPOCHS = 100
WARMUP_EPOCHS = 5
MIN_EPOCHS = 30
PATIENCE = 15
LEARNING_RATE = 3e-4
WEIGHT_DECAY = 1e-2
THRESHOLD = 0.5
""")
code(r"""
def load_manifest(path, root, protocol, provenance=''):
    if protocol not in {'source_separated', 'development'}:
        raise ValueError('Unknown protocol')
    with Path(path).open(newline='') as stream:
        reader = csv.DictReader(stream)
        if not {'path', 'label', 'surface', 'parent_id', 'split'} <= set(reader.fieldnames or []):
            raise ValueError('Manifest needs path,label,surface,parent_id,split')
        rows = list(reader)
    if not rows:
        raise ValueError('Empty manifest')
    root = Path(root).resolve()
    seen_paths, hash_splits, parent_splits = set(), {}, {}
    for row in rows:
        row['split'] = {'val': 'validation'}.get(row['split'], row['split'])
        if row['split'] not in {'train', 'validation', 'test'} or row['label'] not in {'0', '1'}:
            raise ValueError('Invalid split or binary label')
        if row['surface'] not in {'deck', 'wall', 'pavement'}:
            raise ValueError('Unknown surface')
        image_path = (root / row['path']).resolve()
        if not image_path.is_relative_to(root) or not image_path.is_file():
            raise ValueError(f'Image missing or outside DATA_ROOT: {image_path}')
        if image_path in seen_paths:
            raise ValueError('Repeated image path')
        seen_paths.add(image_path)
        digest = hashlib.sha256(image_path.read_bytes()).hexdigest()
        previous = hash_splits.setdefault(digest, row['split'])
        if previous != row['split']:
            raise ValueError('Exact duplicate image crosses splits')
        with Image.open(image_path) as image:
            image.verify()
        parent = row['parent_id'].strip()
        if protocol == 'source_separated':
            if not parent or not provenance.strip():
                raise ValueError('Verified parent IDs and provenance are required')
            if parent_splits.setdefault(parent, row['split']) != row['split']:
                raise ValueError(f'Parent leakage: {parent}')
        row['label'] = int(row['label'])
    groups = {s: [r for r in rows if r['split'] == s] for s in ('train', 'validation', 'test')}
    required = ('train', 'validation', 'test') if protocol == 'source_separated' else ('train', 'validation')
    for split in required:
        if {r['label'] for r in groups[split]} != {0, 1}:
            raise ValueError(f'{split} must contain both classes')
    return groups

class CrackDataset(Dataset):
    def __init__(self, rows, root, transform):
        self.rows, self.root, self.transform = rows, Path(root), transform
    def __len__(self):
        return len(self.rows)
    def __getitem__(self, index):
        row = self.rows[index]
        with Image.open(self.root / row['path']) as image:
            tensor = self.transform(image.convert('RGB'))
        return tensor, torch.tensor([row['label']], dtype=torch.float32)

def training_normalization(rows, root):
    transform = T.Compose([T.Resize(256), T.CenterCrop(224), T.ToTensor()])
    loader = DataLoader(CrackDataset(rows, root, transform), batch_size=BATCH_SIZE)
    sums, squares, pixels = torch.zeros(3, dtype=torch.float64), torch.zeros(3, dtype=torch.float64), 0
    for images, _ in loader:
        images = images.double()
        sums += images.sum((0, 2, 3))
        squares += images.square().sum((0, 2, 3))
        pixels += images.shape[0] * images.shape[2] * images.shape[3]
    mean = sums / pixels
    std = (squares / pixels - mean.square()).clamp_min(1e-8).sqrt()
    return mean.tolist(), std.tolist()

def make_transforms(mean, std):
    train = T.Compose([T.RandomResizedCrop(224, scale=(0.85, 1.0)),
        T.RandomHorizontalFlip(), T.RandomVerticalFlip(),
        T.RandomRotation(15, interpolation=T.InterpolationMode.BILINEAR, fill=tuple(round(m*255) for m in mean)),
        T.ColorJitter(brightness=0.15, contrast=0.15), T.ToTensor(), T.Normalize(mean, std)])
    evaluation = T.Compose([T.Resize(256), T.CenterCrop(224), T.ToTensor(), T.Normalize(mean, std)])
    return train, evaluation

def binary_metrics(labels, probabilities, threshold=0.5):
    labels, probabilities = np.asarray(labels).reshape(-1), np.asarray(probabilities).reshape(-1)
    predictions = probabilities >= threshold
    tn, fp, fn, tp = confusion_matrix(labels, predictions, labels=[0, 1]).ravel()
    both = len(np.unique(labels)) == 2
    return dict(accuracy=float(accuracy_score(labels, predictions)),
        balanced_accuracy=float(balanced_accuracy_score(labels, predictions)),
        precision=float(precision_score(labels, predictions, zero_division=0)),
        recall=float(recall_score(labels, predictions, zero_division=0)),
        specificity=float(tn / (tn + fp)) if tn + fp else None,
        f1=float(f1_score(labels, predictions, zero_division=0)),
        macro_f1=float(f1_score(labels, predictions, labels=[0, 1], average='macro', zero_division=0)),
        roc_auc=float(roc_auc_score(labels, probabilities)) if both else None,
        average_precision=float(average_precision_score(labels, probabilities)) if both else None,
        confusion_matrix=[[int(tn), int(fp)], [int(fn), int(tp)]])

@torch.inference_mode()
def evaluate(net, loader, criterion):
    net.eval()
    labels, probabilities, total = [], [], 0.
    for images, targets in loader:
        images, targets = images.to(DEVICE), targets.to(DEVICE)
        logits = net(images)
        total += criterion(logits, targets).item() * len(images)
        labels.extend(targets.cpu().flatten().tolist())
        probabilities.extend(logits.sigmoid().cpu().flatten().tolist())
    return total / len(loader.dataset), binary_metrics(labels, probabilities), probabilities
""")
md("""
## 7. Training, checkpointing, and held-out evaluation

Selection uses validation **macro-F1**, following Phase 3. Weighted BCE uses only
training class counts. AMP is enabled on CUDA; CPU/MPS use float32. Every run gets
a new output folder, including its manifest, normalization, settings, history,
best weights, and predictions. Checkpoints include inference metadata. They are
inference checkpoints, not exact mid-epoch resume snapshots.

Average precision is explicitly reported as AP, a common PR summary; it is not
silently relabeled as trapezoidal PR-AUC. Repeating seeds measures optimization
variability, not uncertainty from independent parent photographs.
""")
code(r"""
def train_one_seed(groups, mean, std, seed, run_dir):
    seed_everything(seed)
    train_tf, eval_tf = make_transforms(mean, std)
    loaders = {split: DataLoader(CrackDataset(rows, DATA_ROOT,
                    train_tf if split == 'train' else eval_tf), batch_size=BATCH_SIZE,
                    shuffle=split == 'train', num_workers=0,
                    generator=torch.Generator().manual_seed(seed))
               for split, rows in groups.items() if rows}
    net = CrackFusionTiny().to(DEVICE)
    positive = sum(r['label'] for r in groups['train'])
    weight = (len(groups['train']) - positive) / positive
    criterion = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([weight], device=DEVICE))
    optimizer = torch.optim.AdamW(net.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    scaler = torch.amp.GradScaler('cuda', enabled=DEVICE.type == 'cuda')
    accumulation = EFFECTIVE_BATCH // BATCH_SIZE
    best, stale, history = -1., 0, []
    checkpoint_path = run_dir / f'best_seed_{seed}.pt'
    for epoch in range(MAX_EPOCHS):
        factor = ((epoch + 1) / WARMUP_EPOCHS if epoch < WARMUP_EPOCHS else
                  0.5 * (1 + math.cos(math.pi * (epoch - WARMUP_EPOCHS) /
                                     max(1, MAX_EPOCHS - WARMUP_EPOCHS - 1))))
        for group in optimizer.param_groups:
            group['lr'] = LEARNING_RATE * factor
        net.train()
        optimizer.zero_grad(set_to_none=True)
        total = 0.
        for index, (images, targets) in enumerate(loaders['train']):
            images, targets = images.to(DEVICE), targets.to(DEVICE)
            start = (index // accumulation) * accumulation * BATCH_SIZE
            group_size = min(EFFECTIVE_BATCH, len(groups['train']) - start)
            with torch.autocast(device_type=DEVICE.type, enabled=DEVICE.type == 'cuda'):
                loss = criterion(net(images), targets)
            if not torch.isfinite(loss):
                raise FloatingPointError('Nonfinite training loss')
            scaler.scale(loss * len(images) / group_size).backward()
            if (index + 1) % accumulation == 0 or index + 1 == len(loaders['train']):
                scaler.unscale_(optimizer)
                nn.utils.clip_grad_norm_(net.parameters(), 1.0, error_if_nonfinite=True)
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad(set_to_none=True)
            total += loss.item() * len(images)
        val_loss, metrics, _ = evaluate(net, loaders['validation'], criterion)
        record = dict(epoch=epoch+1, train_loss=total/len(groups['train']),
                      validation_loss=val_loss, lr=optimizer.param_groups[0]['lr'], **metrics)
        history.append(record)
        print(f"seed={seed} epoch={epoch+1} loss={record['train_loss']:.4f} val_macro_f1={metrics['macro_f1']:.4f}")
        if metrics['macro_f1'] > best:
            best, stale = metrics['macro_f1'], 0
            torch.save(dict(model=net.state_dict(), seed=seed, epoch=epoch+1,
                architecture='CrackFusionTiny-v1', parameters=PARAMETERS,
                mean=mean, std=std, threshold=THRESHOLD, protocol=PROTOCOL,
                validation_metrics=metrics), checkpoint_path)
        else:
            stale += 1
        (run_dir / f'history_seed_{seed}.json').write_text(json.dumps(history, indent=2))
        if epoch + 1 >= MIN_EPOCHS and stale >= PATIENCE:
            break
    checkpoint = torch.load(checkpoint_path, map_location=DEVICE, weights_only=True)
    net.load_state_dict(checkpoint['model'])
    split = 'test' if RUN_TEST else 'validation'
    _, metrics, probabilities = evaluate(net, loaders[split], criterion)
    per_surface = {}
    for surface in ('deck', 'wall', 'pavement'):
        selected = [(r['label'], p) for r, p in zip(groups[split], probabilities) if r['surface'] == surface]
        if selected:
            ys, ps = zip(*selected)
            per_surface[surface] = binary_metrics(ys, ps)
    result = dict(seed=seed, split=split, protocol=PROTOCOL, metrics=metrics, per_surface=per_surface)
    (run_dir / f'metrics_seed_{seed}.json').write_text(json.dumps(result, indent=2))
    with (run_dir / f'predictions_seed_{seed}.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=['path', 'label', 'surface', 'parent_id', 'probability', 'prediction'])
        writer.writeheader()
        for row, probability in zip(groups[split], probabilities):
            writer.writerow({k: row[k] for k in ('path', 'label', 'surface', 'parent_id')} |
                            dict(probability=probability, prediction=int(probability >= THRESHOLD)))
    return result

def run_experiment():
    if BATCH_SIZE <= 0 or EFFECTIVE_BATCH % BATCH_SIZE or MAX_EPOCHS < 1:
        raise ValueError('Batch size must divide effective batch; epochs must be positive')
    if RUN_TEST and PROTOCOL != 'source_separated':
        raise ValueError('Development splits cannot produce research test results')
    groups = load_manifest(MANIFEST, DATA_ROOT, PROTOCOL, PARENT_ID_PROVENANCE)
    mean, std = training_normalization(groups['train'], DATA_ROOT)
    run_dir = OUTPUT_ROOT / (time.strftime('%Y%m%d_%H%M%S') + f'_{time.time_ns() % 1000000000:09d}')
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / 'manifest.csv').write_bytes(MANIFEST.read_bytes())
    configuration = {key: globals()[key] for key in ('PROTOCOL', 'PARENT_ID_PROVENANCE', 'SEEDS',
        'BATCH_SIZE', 'EFFECTIVE_BATCH', 'MAX_EPOCHS', 'WARMUP_EPOCHS', 'MIN_EPOCHS',
        'PATIENCE', 'LEARNING_RATE', 'WEIGHT_DECAY', 'THRESHOLD', 'RUN_TEST')}
    configuration.update(mean=mean, std=std, parameters=PARAMETERS,
        torch=str(torch.__version__), torchvision=str(torchvision.__version__), device=str(DEVICE),
        manifest_sha256=hashlib.sha256(MANIFEST.read_bytes()).hexdigest())
    (run_dir / 'configuration.json').write_text(json.dumps(configuration, indent=2))
    results = [train_one_seed(groups, mean, std, seed, run_dir) for seed in SEEDS]
    summary = {}
    for key in ('macro_f1', 'f1', 'recall', 'balanced_accuracy', 'average_precision'):
        values = [r['metrics'][key] for r in results]
        summary[key] = dict(mean=statistics.mean(values),
                            seed_std=statistics.stdev(values) if len(values) > 1 else None)
    (run_dir / 'summary.json').write_text(json.dumps(summary, indent=2))
    print('Saved:', run_dir.resolve())
    return results, summary

if RUN_TRAINING:
    experiment_results, experiment_summary = run_experiment()
    print(json.dumps(experiment_summary, indent=2))
else:
    print('Real-data training disabled. Set DATA_ROOT, MANIFEST, provenance, and RUN_TRAINING.')
""")
md("""
## 8. Validate the data/training path without SDNET

A temporary image fixture checks the CSV loader, duplicate/parent leakage rejection,
normalization, partial gradient-accumulation groups, one training epoch, metrics,
checkpoint loading, and per-image prediction export. Images and weights are removed
with the temporary directory. This is an integration check, not research training.
""")
code(r"""
def validate_training_pipeline():
    global DATA_ROOT, MANIFEST, OUTPUT_ROOT, PROTOCOL, PARENT_ID_PROVENANCE
    global BATCH_SIZE, EFFECTIVE_BATCH, MAX_EPOCHS, SEEDS, RUN_TEST
    names = ('DATA_ROOT', 'MANIFEST', 'OUTPUT_ROOT', 'PROTOCOL', 'PARENT_ID_PROVENANCE',
             'BATCH_SIZE', 'EFFECTIVE_BATCH', 'MAX_EPOCHS', 'SEEDS', 'RUN_TEST')
    saved = {name: globals()[name] for name in names}
    try:
        with TemporaryDirectory() as temporary:
            DATA_ROOT = Path(temporary)
            MANIFEST, OUTPUT_ROOT = DATA_ROOT / 'manifest.csv', DATA_ROOT / 'runs'
            PROTOCOL, PARENT_ID_PROVENANCE = 'source_separated', 'Artificial fixture IDs only'
            BATCH_SIZE, EFFECTIVE_BATCH, MAX_EPOCHS, SEEDS, RUN_TEST = 2, 4, 1, (42,), True
            rng = np.random.default_rng(7)
            rows = []
            for split, count in [('train', 6), ('validation', 2), ('test', 2)]:
                for index in range(count):
                    name = f'{split}_{index}.png'
                    Image.fromarray(rng.integers(0, 256, (256, 256, 3), dtype=np.uint8)).save(DATA_ROOT / name)
                    rows.append(dict(path=name, label=index % 2, surface='deck',
                                     parent_id=f'{split}_{index}', split=split))
            def write_rows(items):
                with MANIFEST.open('w', newline='') as stream:
                    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                    writer.writeheader(); writer.writerows(items)
            write_rows(rows)
            results, _ = run_experiment()
            assert results[0]['split'] == 'test'
            assert results[0]['metrics']['confusion_matrix']
            checkpoint = next(OUTPUT_ROOT.rglob('*.pt'))
            assert torch.load(checkpoint, weights_only=True, map_location='cpu')['parameters'] == PARAMETERS
            predictions = next(OUTPUT_ROOT.rglob('predictions*.csv'))
            with predictions.open() as stream:
                assert len(list(csv.DictReader(stream))) == 2
            for kind in ('parent', 'duplicate'):
                broken = [dict(row) for row in rows]
                if kind == 'parent':
                    broken[-1]['parent_id'] = broken[0]['parent_id']
                else:
                    duplicate = DATA_ROOT / 'duplicate.png'
                    duplicate.write_bytes((DATA_ROOT / rows[0]['path']).read_bytes())
                    broken[-1]['path'] = duplicate.name
                write_rows(broken)
                try:
                    load_manifest(MANIFEST, DATA_ROOT, PROTOCOL, PARENT_ID_PROVENANCE)
                except ValueError as error:
                    assert 'leakage' in str(error).lower() or 'duplicate' in str(error).lower()
                else:
                    raise AssertionError(f'{kind} leakage was accepted')
    finally:
        globals().update(saved)
    return 'passed: train/evaluate/save/predict, parent and exact-duplicate rejection'

validation_report['training_pipeline'] = validate_training_pipeline()
print(validation_report['training_pipeline'])
""")
md("""
## 9. Load trained weights and classify your own image

Use a real-data checkpoint from section 7. A single image prediction is a screening
output, not a crack-width measurement or structural diagnosis. The returned sigmoid
score is not guaranteed calibrated, especially with class-weighted BCE.
""")
code(r"""
def predict_image(checkpoint_path, image_path):
    checkpoint = torch.load(checkpoint_path, map_location='cpu', weights_only=True)
    if checkpoint.get('architecture') != 'CrackFusionTiny-v1':
        raise ValueError('Wrong checkpoint architecture')
    net = CrackFusionTiny().to(DEVICE).eval()
    net.load_state_dict(checkpoint['model'])
    _, transform = make_transforms(checkpoint['mean'], checkpoint['std'])
    with Image.open(image_path) as image:
        tensor = transform(image.convert('RGB')).unsqueeze(0).to(DEVICE)
    with torch.inference_mode():
        score = net(tensor).sigmoid().item()
    return dict(crack_score=score, prediction='crack' if score >= checkpoint['threshold'] else 'no crack',
                threshold=checkpoint['threshold'], training_protocol=checkpoint['protocol'])

# predict_image('output/crackfusion_tiny/<run>/best_seed_42.pt', '/content/example.jpg')

# Verify the public inference function with a temporary, explicitly untrained checkpoint.
with TemporaryDirectory() as temporary:
    temporary = Path(temporary)
    inference_net = CrackFusionTiny().eval()
    torch.save(dict(model=inference_net.state_dict(), architecture='CrackFusionTiny-v1',
        mean=[0.5]*3, std=[0.25]*3, threshold=0.5, protocol='synthetic_check'), temporary / 'model.pt')
    Image.new('RGB', (256, 256), color=(140, 140, 140)).save(temporary / 'image.png')
    inference_result = predict_image(temporary / 'model.pt', temporary / 'image.png')
    assert 0 <= inference_result['crack_score'] <= 1
    assert inference_result['training_protocol'] == 'synthetic_check'
    _, inference_transform = make_transforms([0.5]*3, [0.25]*3)
    with Image.open(temporary / 'image.png') as image, torch.inference_mode():
        expected_score = inference_net(inference_transform(image).unsqueeze(0)).sigmoid().item()
    assert abs(inference_result['crack_score'] - expected_score) < 1e-4
validation_report['custom_image_inference'] = 'passed'
print('Custom-image preprocessing and checkpoint inference: passed')
""")
md("""
## 10. Measured inference latency and validation report

Random weights are sufficient for timing this fixed graph. Timing uses batch 1,
float32, warm-up, and device synchronization; it excludes image preprocessing.
Parameter memory is not peak runtime memory. CUDA peak allocation is measured when
available. CPU/MPS peak memory and MACs/FLOPs are left unreported, not estimated.
""")
code(r"""
def synchronize():
    if DEVICE.type == 'cuda':
        torch.cuda.synchronize()
    elif DEVICE.type == 'mps':
        torch.mps.synchronize()

timing_model = CrackFusionTiny().to(DEVICE).eval()
timing_input = torch.randn(1, 3, 224, 224, device=DEVICE)
durations = []
with torch.inference_mode():
    for _ in range(5):
        timing_model(timing_input)
    synchronize()
    if DEVICE.type == 'cuda':
        torch.cuda.reset_peak_memory_stats()
    for _ in range(20):
        synchronize(); start = time.perf_counter()
        timing_model(timing_input)
        synchronize(); durations.append((time.perf_counter() - start) * 1000)
validation_report.update(parameters=PARAMETERS, device=str(DEVICE),
    median_batch1_ms=statistics.median(durations), torch=str(torch.__version__),
    cuda_peak_allocated_bytes=torch.cuda.max_memory_allocated() if DEVICE.type == 'cuda' else None,
    research_accuracy_measured=False)
print(json.dumps(validation_report, indent=2))
del timing_model
""")
md("""
## 11. What this notebook establishes

The saved outputs document model and training-pipeline validation. Real research
claims still require verified parent groups, final SDNET training, comparable
baselines, three held-out-surface experiments, and parent-cluster confidence intervals.
Removing branches from a trained model is not a substitute for retraining matched
baselines. Attribution visualizations also require trained weights and separate
validation; exposed feature maps alone are not explanations.

The exact tensor design is preserved with a final encoder normalization and zero
stochastic depth explicitly documented. The earlier 1–3M estimate must be updated
in future methodology revisions to the measured count. The notebook does not modify
the already-approved methodology PDF.
""")

notebook = nbf.v4.new_notebook(cells=cells, metadata={
    'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
    'language_info': {'name': 'python', 'version': '3.12'},
    'colab': {'name': '06_crackfusion_tiny_implementation.ipynb'}})
destination = Path(__file__).resolve().parents[1] / 'notebooks' / '06_crackfusion_tiny_implementation.ipynb'
nbf.validate(notebook)
nbf.write(notebook, destination)
print(destination)

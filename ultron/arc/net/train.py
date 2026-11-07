"""Training Ultron's network, and answering with it (votes across augmented views).

The puzzles: its practice half (examples and test answers may be learned), minus a tenth
kept back for calibration (examples only, like held-out puzzles), its held-out half
(examples only), and its dreams. The network answers a tested puzzle in every augmented
view; the answers are mapped back and counted. The judge (arc/judge.py) uses an answer
only when at least k views agree, with k chosen on the calibration puzzles, never on the
held-out ones.

    python -m ultron net train [--quick] [--device cuda] [--steps N]
"""

import collections
import copy
import json
import os
import time

import numpy as np
import torch
from torch.nn import functional as F

from .. import data as arcdata
from .. import dreams as arcdreams
from .. import loop
from . import data
from .model import Recursive

CKPT = os.path.join(arcdata.ROOT, "brain", "net.pt")
REPORT = os.path.join(arcdata.ROOT, "reports", "net_training.md")

CONFIGS = {
    # a few minutes on a CPU: checks the whole pipeline, learns little
    "quick": dict(hidden=64, heads=4, layers=2, H=2, L=2, sup=2, views=4, dreams=60,
                  steps=200, batch=16, lr=1e-3, puzzle_lr=1e-2, warmup=20, ema=0.99),
    # sized for one modern GPU for about a day in bfloat16 (roughly 2e19 operations; TRM's
    # published runs used several GPUs for days): 64 views per real puzzle, 1 per dream
    "full": dict(hidden=512, heads=8, layers=2, H=3, L=6, sup=8, views=64, dreams=20000,
                 steps=40000, batch=128, lr=1e-4, puzzle_lr=1e-2, warmup=2000, ema=0.999),
}


def split(quick):
    tasks, practice, held = loop.halves(quick)
    calib = practice[::10]
    learn = [t for t in practice if t not in set(calib)]
    return tasks, learn, calib, held


def build(cfg, quick, seed=0):
    tasks, learn, calib, held = split(quick)
    words = loop.load()["words"] if not quick else []
    dreamt = arcdreams.make(tasks, learn, words, n=cfg["dreams"], seed=seed) \
        if cfg["dreams"] else []
    ds = data.pairs(tasks, learn, calib + held, dreamt, n_views=cfg["views"], seed=seed)
    return tasks, learn, calib, held, ds


def _lr(step, cfg):
    return min(1.0, (step + 1) / cfg["warmup"])


def train(quick=False, device="cpu", steps=None, seed=0, path=CKPT, log=print):
    cfg = dict(CONFIGS["quick" if quick else "full"])
    if steps:
        cfg["steps"] = steps
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    tasks, learn, calib, held, ds = build(cfg, quick, seed)
    model = Recursive(len(ds["ids"]), cfg["hidden"], cfg["heads"], cfg["layers"], cfg["H"],
                      cfg["L"]).to(device)
    ema = copy.deepcopy(model).eval()
    body = [p for n, p in model.named_parameters() if not n.startswith("puzzle.")]
    opt = torch.optim.AdamW([{"params": body, "lr": cfg["lr"], "weight_decay": 0.1},
                             {"params": model.puzzle.parameters(), "lr": cfg["puzzle_lr"],
                              "weight_decay": 0.1}], betas=(0.9, 0.95))
    base = [g["lr"] for g in opt.param_groups]
    X = torch.from_numpy(ds["x"])
    Y = torch.from_numpy(ds["y"])
    P = torch.from_numpy(ds["puzzle"])
    started, history = time.time(), []
    log(f"{len(ds['ids'])} puzzle views, {len(X)} training pairs, "
        f"{sum(p.numel() for p in model.parameters()):,} parameters, device {device}")
    for step in range(cfg["steps"]):
        idx = torch.from_numpy(rng.integers(0, len(X), cfg["batch"]))
        x, y_t, pid = X[idx].long().to(device), Y[idx].long().to(device), P[idx].to(device)
        for g, b in zip(opt.param_groups, base):
            g["lr"] = b * _lr(step, cfg)
        y = z = None
        for s in range(cfg["sup"]):
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16,
                                enabled=device.startswith("cuda")):
                emb = model.embed(x, pid)
                if y is None:
                    y, z = model.start(emb)
                y, z, logits = model.step(emb, y, z)
                loss = F.cross_entropy(logits.float().reshape(-1, data.VOCAB), y_t.reshape(-1))
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            with torch.no_grad():
                for pe, pm in zip(ema.parameters(), model.parameters()):
                    pe.mul_(cfg["ema"]).add_(pm.detach(), alpha=1 - cfg["ema"])
            y, z = y.detach(), z.detach()
        if step % max(1, cfg["steps"] // 20) == 0 or step == cfg["steps"] - 1:
            exact = (logits.argmax(-1).view_as(y_t) == y_t).flatten(1).all(1).float().mean()
            history.append((step, loss.item(), exact.item()))
            log(f"step {step}: loss {loss.item():.3f}, exact {exact.item():.0%}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    torch.save({"cfg": cfg, "state": ema.state_dict(), "ids": ds["ids"],
                "views": [(k, perm.tolist()) for k, perm in ds["views"]],
                "split": {"learn": learn, "calib": calib, "held": held}, "quick": quick},
               path)
    _report(cfg, ds, history, time.time() - started, device, quick)
    return path


def _report(cfg, ds, history, seconds, device, quick):
    lines = ["# Training Ultron's network (engine 2)", "",
             f"Run: {'quick (CPU smoke test)' if quick else 'full'}, device {device}, "
             f"{seconds / 60:.0f} minutes. {len(ds['ids'])} puzzle views, "
             f"{len(ds['x'])} training pairs. Config: `{json.dumps(cfg)}`.", "",
             "| Step | Loss | Training pairs exactly right |", "|---|---|---|"]
    lines += [f"| {s} | {l:.3f} | {e:.0%} |" for s, l, e in history]
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w") as f:
        f.write("\n".join(lines) + "\n")


def load(path=CKPT, device="cpu"):
    ck = torch.load(path, map_location=device, weights_only=False)
    cfg = ck["cfg"]
    model = Recursive(len(ck["ids"]), cfg["hidden"], cfg["heads"], cfg["layers"], cfg["H"],
                      cfg["L"]).to(device)
    model.load_state_dict(ck["state"])
    model.eval()
    ck["views"] = [(k, np.array(p)) for k, p in ck["views"]]
    return model, ck


def votes(model, ck, tasks, names, device="cpu", batch=64):
    """{(task, test index): [(grid, votes)], most votes first} from every view."""
    ds = {"ids": ck["ids"], "views": ck["views"]}
    items = data.test_inputs(tasks, names, ds)
    count = collections.defaultdict(collections.Counter)
    grids = {}
    for s in range(0, len(items), batch):
        chunk = items[s:s + batch]
        x = torch.from_numpy(np.stack([it[4] for it in chunk])).long().to(device)
        pid = torch.tensor([it[3] for it in chunk], device=device)
        pred = model.predict(x, pid, ck["cfg"]["sup"]).cpu().numpy()
        for (t, j, v, _, _), p in zip(chunk, pred):
            g = data.decode(p)
            if g is None:
                continue
            g = data.undo(g, ck["views"][v])
            key = (g.shape, g.tobytes())
            grids[key] = g
            count[(t, j)][key] += 1
    return {tj: [(grids[k], n) for k, n in c.most_common()] for tj, c in count.items()}


def choose_k(tasks, calib, v, n_views, want=0.95):
    """The smallest k (agreeing views) at which the net's answers on the calibration
    puzzles are right at least `want` of the time; n_views + 1 (never answer) if none."""
    for k in range(1, n_views + 1):
        right = wrong = 0
        for t in calib:
            for j, (_, o) in enumerate(tasks[t]["test"]):
                top = v.get((t, j))
                if not top or top[0][1] < k:
                    continue
                if np.array_equal(top[0][0], o):
                    right += 1
                else:
                    wrong += 1
        if right + wrong and right / (right + wrong) >= want:
            return k
    return n_views + 1

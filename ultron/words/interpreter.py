"""The interpreter: a small network that carries out one word on one picture.

It reads the picture as tokens (state.py), adds the word's vector (operation + argument)
to every cell, thinks with a couple of transformer layers used a few times over, and
writes the next picture. It is trained from scratch, like everything in Ultron. The
result is snapped to exact colours, so the next word always starts from a real picture.
"""

import math

import numpy as np
import torch
from torch import nn

from ..arc.net.model import Block
from .state import VOCAB, decode, encode


class Interpreter(nn.Module):
    def __init__(self, n_ops, n_args, size, hidden=128, heads=4, layers=2, loops=3):
        super().__init__()
        self.size, self.hidden, self.loops = size, hidden, loops
        self.cfg = dict(n_ops=n_ops, n_args=n_args, size=size, hidden=hidden, heads=heads,
                        layers=layers, loops=loops)
        std = 1 / math.sqrt(hidden)
        self.tok = nn.Embedding(VOCAB, hidden)
        self.row = nn.Parameter(torch.randn(size, hidden) * std)
        self.col = nn.Parameter(torch.randn(size, hidden) * std)
        self.op = nn.Embedding(n_ops, hidden)
        self.arg = nn.Embedding(n_args, hidden)
        for e in (self.tok, self.op, self.arg):
            nn.init.normal_(e.weight, std=std)
        self.net = nn.Sequential(*[Block(hidden, heads) for _ in range(layers)])
        self.out = nn.Linear(hidden, VOCAB, bias=False)

    def word(self, op_id, arg_id):
        return self.op(op_id) + self.arg(arg_id)

    def forward(self, tokens, op_id=None, arg_id=None, word=None):
        """tokens (B, size*size), a word per picture -> logits (B, size*size, VOCAB)."""
        w = self.word(op_id, arg_id) if word is None else word
        pos = (self.row[:, None] + self.col[None]).reshape(1, -1, self.hidden)
        x = self.tok(tokens) + pos + w[:, None]
        x = torch.cat([w[:, None], x], dim=1) * math.sqrt(self.hidden) * 0.5
        h = self.net(x)
        for _ in range(self.loops - 1):
            h = self.net(h + x)
        return self.out(h[:, 1:])

    @torch.no_grad()
    def run(self, grids, ids, batch=512):
        """Carry out one word on each picture: exact pictures back (None where the answer
        isn't a picture). ids = [(op_id, arg_id), ...], one per picture."""
        self.eval()
        dev = self.tok.weight.device
        out = []
        for i in range(0, len(grids), batch):
            toks = torch.as_tensor(np.stack([encode(g, self.size).ravel()
                                             for g in grids[i:i + batch]]), device=dev)
            op, arg = torch.as_tensor(ids[i:i + batch], device=dev).T
            pred = self(toks, op, arg).argmax(-1).cpu().numpy()
            out += [decode(p, self.size) for p in pred]
        return out


def save(model, path, **extra):
    torch.save({"cfg": model.cfg, "state": model.state_dict(), **extra}, path)


def load(path, device="cpu"):
    ck = torch.load(path, map_location=device, weights_only=False)
    model = Interpreter(**ck["cfg"]).to(device)
    model.load_state_dict(ck["state"])
    return model, ck

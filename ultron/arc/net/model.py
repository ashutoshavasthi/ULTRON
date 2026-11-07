"""The recursive network (after TRM, arXiv 2510.04871), trained by Ultron from scratch.

One tiny network (a couple of transformer layers) is used over and over. Given the
puzzle (its input grid and its learned puzzle embedding, x), it keeps an answer y and a
latent reasoning state z, and improves them in cycles:

    repeat H times:   repeat L times: z = net(x + y + z)      (think)
                      y = net(y + z)                           (revise the answer)

Only the last cycle is trained through; the earlier ones run without gradients (as in
TRM). Training uses deep supervision: the answer is scored after every supervision step,
and y and z are carried (detached) into the next step, so the network learns to improve
its own answer step by step.
"""

import math

import torch
from torch import nn
from torch.nn import functional as F

from .data import SIZE, VOCAB


class RMSNorm(nn.Module):
    def __init__(self, d, eps=1e-6):
        super().__init__()
        self.eps = eps
        self.w = nn.Parameter(torch.ones(d))

    def forward(self, x):
        return self.w * x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)


class Block(nn.Module):
    """Self-attention over the whole grid, then a gated MLP (post-norm, as TRM)."""

    def __init__(self, d, heads, mult=4):
        super().__init__()
        self.heads = heads
        self.qkv = nn.Linear(d, 3 * d, bias=False)
        self.proj = nn.Linear(d, d, bias=False)
        self.gate = nn.Linear(d, 2 * mult * d, bias=False)
        self.down = nn.Linear(mult * d, d, bias=False)
        self.n1, self.n2 = RMSNorm(d), RMSNorm(d)

    def forward(self, x):
        b, n, d = x.shape
        q, k, v = self.qkv(x).view(b, n, 3, self.heads, d // self.heads).unbind(2)
        a = F.scaled_dot_product_attention(q.transpose(1, 2), k.transpose(1, 2),
                                           v.transpose(1, 2))
        x = self.n1(x + self.proj(a.transpose(1, 2).reshape(b, n, d)))
        g, u = self.gate(x).chunk(2, dim=-1)
        return self.n2(x + self.down(F.silu(g) * u))


class Recursive(nn.Module):
    def __init__(self, n_puzzles, hidden=256, heads=4, layers=2, H=3, L=6, prefix=1):
        super().__init__()
        self.H, self.L, self.prefix, self.hidden = H, L, prefix, hidden
        # tokens, positions and puzzles on the same scale (as TRM's code does), so where a
        # cell is counts as much as what colour it is
        std = 1 / math.sqrt(hidden)
        self.tok = nn.Embedding(VOCAB, hidden)
        nn.init.normal_(self.tok.weight, std=std)
        self.puzzle = nn.Embedding(n_puzzles, prefix * hidden)
        nn.init.zeros_(self.puzzle.weight)
        self.pos = nn.Parameter(torch.randn(prefix + SIZE * SIZE, hidden) * std)
        self.net = nn.Sequential(*[Block(hidden, heads) for _ in range(layers)])
        self.out = nn.Linear(hidden, VOCAB, bias=False)
        self.y0 = nn.Parameter(torch.randn(hidden) * 0.02)
        self.z0 = nn.Parameter(torch.randn(hidden) * 0.02)

    def embed(self, tokens, pid):
        """x: the puzzle (its learned embedding, then its input grid), with positions."""
        b = tokens.shape[0]
        grid = self.tok(tokens.view(b, -1))
        pz = self.puzzle(pid).view(b, self.prefix, self.hidden)
        x = torch.cat([pz, grid], dim=1) + self.pos
        return math.sqrt(self.hidden) * 0.7071 * x

    def start(self, x):
        return self.y0.expand_as(x).clone(), self.z0.expand_as(x).clone()

    def _cycle(self, x, y, z):
        for _ in range(self.L):
            z = self.net(x + y + z)
        return self.net(y + z), z

    def step(self, x, y, z):
        """One supervision step: H cycles, gradients only through the last."""
        with torch.no_grad():
            for _ in range(self.H - 1):
                y, z = self._cycle(x, y, z)
        y, z = self._cycle(x, y, z)
        logits = self.out(y[:, self.prefix:])            # (batch, 900, vocab)
        return y, z, logits

    @torch.no_grad()
    def predict(self, tokens, pid, steps):
        x = self.embed(tokens, pid)
        y, z = self.start(x)
        for _ in range(steps):
            y, z, logits = self.step(x, y, z)
        return logits.argmax(-1).view(-1, SIZE, SIZE)

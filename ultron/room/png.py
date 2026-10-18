"""A small PNG writer (numpy, zlib and struct only), for pictures of the room."""

import struct
import zlib

import numpy as np


def _chunk(kind, data):
    body = kind + data
    return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)


def encode(rgb):
    """rgb: an (h, w, 3) array of brightness 0-1. Returns the PNG file's bytes."""
    a = (np.clip(np.asarray(rgb, dtype=float), 0.0, 1.0) * 255 + 0.5).astype(np.uint8)
    h, w, _ = a.shape
    raw = b"".join(b"\x00" + a[r].tobytes() for r in range(h))
    return (b"\x89PNG\r\n\x1a\n"
            + _chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + _chunk(b"IDAT", zlib.compress(raw, 9))
            + _chunk(b"IEND", b""))


def bigger(rgb, k):
    return np.repeat(np.repeat(rgb, k, axis=0), k, axis=1)

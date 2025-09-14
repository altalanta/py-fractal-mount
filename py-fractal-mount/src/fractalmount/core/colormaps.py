from __future__ import annotations

import numpy as np


def _lerp(a: np.ndarray, b: np.ndarray, t: np.ndarray) -> np.ndarray:
    return a + (b - a) * t[..., None]


def colormap(name: str, h: np.ndarray, slope: np.ndarray | None = None) -> np.ndarray:
    name = name.lower()
    if name == "alpine":
        c0 = np.array([0.1, 0.2, 0.5])
        c1 = np.array([0.1, 0.6, 0.3])
        c2 = np.array([0.6, 0.5, 0.4])
        c3 = np.array([0.95, 0.95, 0.95])
        a = _lerp(c0, c1, np.clip(h * 2.0, 0, 1))
        b = _lerp(c2, c3, np.clip((h - 0.5) * 2.0, 0, 1))
        return np.where(h[..., None] < 0.5, a, b).astype(np.float32)
    if name == "desert":
        c0 = np.array([0.9, 0.8, 0.6])
        c1 = np.array([0.8, 0.6, 0.4])
        return _lerp(c0, c1, h).astype(np.float32)
    if name == "greens":
        c0 = np.array([0.1, 0.3, 0.1])
        c1 = np.array([0.6, 0.9, 0.6])
        return _lerp(c0, c1, h).astype(np.float32)
    g = h[..., None]
    return np.repeat(g, 3, axis=-1).astype(np.float32)


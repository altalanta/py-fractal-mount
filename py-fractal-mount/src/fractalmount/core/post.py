from __future__ import annotations

import numpy as np


def normalize01(h: np.ndarray) -> np.ndarray:
    h = h.astype(np.float32, copy=False)
    mn, mx = float(np.nanmin(h)), float(np.nanmax(h))
    if not np.isfinite(mn) or not np.isfinite(mx) or mx - mn < 1e-8:
        return np.full_like(h, 0.5)
    return ((h - mn) / (mx - mn)).astype(np.float32)


def clamp(h: np.ndarray, vmin: float | None, vmax: float | None) -> np.ndarray:
    if vmin is not None:
        h = np.maximum(h, vmin)
    if vmax is not None:
        h = np.minimum(h, vmax)
    return h.astype(np.float32)


def terrace(h: np.ndarray, steps: int) -> np.ndarray:
    if steps and steps > 1:
        t = np.floor(h * steps) / (steps - 1)
        return np.clip(t, 0.0, 1.0).astype(np.float32)
    return h


def smooth(h: np.ndarray, k: int) -> np.ndarray:
    if k and k > 1:
        if k % 2 == 0:
            k += 1
        x = np.linspace(-1.5, 1.5, k).astype(np.float32)
        w = np.exp(-(x ** 2))
        w /= w.sum()
        pad = k // 2
        hx = np.pad(h, ((0, 0), (pad, pad)), mode="reflect")
        h = np.apply_along_axis(lambda m: np.convolve(m, w, mode="valid"), 1, hx)
        hy = np.pad(h, ((pad, pad), (0, 0)), mode="reflect")
        h = np.apply_along_axis(lambda m: np.convolve(m, w, mode="valid"), 0, hy)
        return h.astype(np.float32)
    return h


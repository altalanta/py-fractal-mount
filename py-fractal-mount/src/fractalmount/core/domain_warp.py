from __future__ import annotations

import numpy as np

from .noise.perlin import perlin2
from .noise.simplex import simplex2


def domain_warp(
    shape: tuple[int, int],
    scale: float,
    perm: np.ndarray,
    strength: float = 0.35,
    warp_scale: float = 1.3,
    base: str = "perlin",
) -> np.ndarray:
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    freq = max(scale, 1e-6)
    x = xx / (w / freq)
    y = yy / (h / freq)

    s1 = warp_scale
    s2 = warp_scale * 0.7
    if base == "perlin":
        n1x = perlin2(x * s1 + 13.1, y * s1 + 7.7, perm)
        n1y = perlin2(x * s1 - 4.2, y * s1 + 9.9, perm)
        xw = x + strength * n1x
        yw = y + strength * n1y
        n2 = perlin2(xw * s2, yw * s2, perm)
    else:
        n1x = simplex2(x * s1 + 13.1, y * s1 + 7.7, perm)
        n1y = simplex2(x * s1 - 4.2, y * s1 + 9.9, perm)
        xw = x + strength * n1x
        yw = y + strength * n1y
        n2 = simplex2(xw * s2, yw * s2, perm)

    out = (n2 + 1.0) * 0.5
    return np.clip(out.astype(np.float32), 0.0, 1.0)


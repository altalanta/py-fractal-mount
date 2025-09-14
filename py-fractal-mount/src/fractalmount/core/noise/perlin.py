from __future__ import annotations

import numpy as np

GRAD2 = np.array(
    [
        [1, 1],
        [-1, 1],
        [1, -1],
        [-1, -1],
        [1, 0],
        [-1, 0],
        [0, 1],
        [0, -1],
    ],
    dtype=np.int32,
)


def fade(t: np.ndarray) -> np.ndarray:
    return t * t * t * (t * (t * 6 - 15) + 10)


def lerp(a: np.ndarray, b: np.ndarray, t: np.ndarray) -> np.ndarray:
    return a + t * (b - a)


def perlin2(x: np.ndarray, y: np.ndarray, perm: np.ndarray) -> np.ndarray:
    xi = np.floor(x).astype(np.int32) & 255
    yi = np.floor(y).astype(np.int32) & 255
    xf = (x - np.floor(x)).astype(np.float32)
    yf = (y - np.floor(y)).astype(np.float32)

    u = fade(xf)
    v = fade(yf)

    aa = perm[perm[xi] + yi] % len(GRAD2)
    ab = perm[perm[xi] + yi + 1] % len(GRAD2)
    ba = perm[perm[xi + 1] + yi] % len(GRAD2)
    bb = perm[perm[xi + 1] + yi + 1] % len(GRAD2)

    g_aa = GRAD2[aa]
    g_ab = GRAD2[ab]
    g_ba = GRAD2[ba]
    g_bb = GRAD2[bb]

    x1 = xf
    y1 = yf
    x2 = xf - 1.0
    y2 = yf
    x3 = xf
    y3 = yf - 1.0
    x4 = xf - 1.0
    y4 = yf - 1.0

    n00 = g_aa[..., 0] * x1 + g_aa[..., 1] * y1
    n10 = g_ba[..., 0] * x2 + g_ba[..., 1] * y2
    n01 = g_ab[..., 0] * x3 + g_ab[..., 1] * y3
    n11 = g_bb[..., 0] * x4 + g_bb[..., 1] * y4

    x_lerp1 = lerp(n00, n10, u)
    x_lerp2 = lerp(n01, n11, u)
    val = lerp(x_lerp1, x_lerp2, v)
    return val.astype(np.float32)


def perlin_noise(shape: tuple[int, int], scale: float, perm: np.ndarray) -> np.ndarray:
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    freq = max(scale, 1e-6)
    x = xx / (w / freq)
    y = yy / (h / freq)
    return perlin2(x, y, perm)


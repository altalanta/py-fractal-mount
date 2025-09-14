from __future__ import annotations

import numpy as np

F2 = 0.5 * (np.sqrt(3.0) - 1.0)
G2 = (3.0 - np.sqrt(3.0)) / 6.0

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


def simplex2(x: np.ndarray, y: np.ndarray, perm: np.ndarray) -> np.ndarray:
    s = (x + y) * F2
    i = np.floor(x + s).astype(np.int32)
    j = np.floor(y + s).astype(np.int32)

    t = (i + j) * G2
    X0 = i - t
    Y0 = j - t
    x0 = x - X0
    y0 = y - Y0

    i1 = (x0 > y0).astype(np.int32)
    j1 = 1 - i1

    x1 = x0 - i1 + G2
    y1 = y0 - j1 + G2
    x2 = x0 - 1.0 + 2.0 * G2
    y2 = y0 - 1.0 + 2.0 * G2

    ii = i & 255
    jj = j & 255

    gi0 = perm[ii + perm[jj]] % len(GRAD2)
    gi1 = perm[ii + i1 + perm[jj + j1]] % len(GRAD2)
    gi2 = perm[ii + 1 + perm[jj + 1]] % len(GRAD2)

    t0 = 0.5 - x0 * x0 - y0 * y0
    t1 = 0.5 - x1 * x1 - y1 * y1
    t2 = 0.5 - x2 * x2 - y2 * y2

    n0 = np.where(t0 > 0, (t0 ** 4) * (GRAD2[gi0][..., 0] * x0 + GRAD2[gi0][..., 1] * y0), 0.0)
    n1 = np.where(t1 > 0, (t1 ** 4) * (GRAD2[gi1][..., 0] * x1 + GRAD2[gi1][..., 1] * y1), 0.0)
    n2 = np.where(t2 > 0, (t2 ** 4) * (GRAD2[gi2][..., 0] * x2 + GRAD2[gi2][..., 1] * y2), 0.0)

    return (70.0 * (n0 + n1 + n2)).astype(np.float32)


def simplex_noise(shape: tuple[int, int], scale: float, perm: np.ndarray) -> np.ndarray:
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    freq = max(scale, 1e-6)
    x = xx / (w / freq)
    y = yy / (h / freq)
    return simplex2(x, y, perm)


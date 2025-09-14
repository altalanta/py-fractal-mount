from __future__ import annotations

import numpy as np

from .seed import rng_from_seed


def diamond_square(size: int, seed: int | str, roughness: float = 0.8) -> np.ndarray:
    assert (size - 1) & (size - 2) == 0, "size must be 2^n + 1"
    rng = rng_from_seed(seed)

    hm = np.zeros((size, size), dtype=np.float32)
    hm[0, 0] = rng.random()
    hm[0, -1] = rng.random()
    hm[-1, 0] = rng.random()
    hm[-1, -1] = rng.random()

    step = size - 1
    amp = 1.0
    while step > 1:
        half = step // 2
        for y in range(half, size - 1, step):
            for x in range(half, size - 1, step):
                c = (
                    hm[y - half, x - half]
                    + hm[y - half, x + half]
                    + hm[y + half, x - half]
                    + hm[y + half, x + half]
                ) * 0.25
                offset = (rng.random() * 2.0 - 1.0) * amp * roughness
                hm[y, x] = c + offset

        for y in range(0, size, half):
            for x in range((y + half) % step, size, step):
                s = 0.0
                c = 0
                if x - half >= 0:
                    s += hm[y, x - half]
                    c += 1
                if x + half < size:
                    s += hm[y, x + half]
                    c += 1
                if y - half >= 0:
                    s += hm[y - half, x]
                    c += 1
                if y + half < size:
                    s += hm[y + half, x]
                    c += 1
                avg = s / max(c, 1)
                offset = (rng.random() * 2.0 - 1.0) * amp * roughness
                hm[y, x] = avg + offset

        step = half
        amp *= 0.5

    mn, mx = float(np.min(hm)), float(np.max(hm))
    if mx - mn < 1e-8:
        hm.fill(0.5)
    else:
        hm = (hm - mn) / (mx - mn)
    return hm.astype(np.float32, copy=False)


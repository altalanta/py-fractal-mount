from __future__ import annotations

import numpy as np


def _seed_to_uint32(seed: int | str) -> np.uint32:
    if isinstance(seed, int):
        return np.uint32(seed & 0xFFFFFFFF)
    h = np.uint32(0x811C9DC5)
    for ch in seed.encode("utf-8"):
        h ^= np.uint32(ch)
        h = np.uint32((h * np.uint32(0x01000193)) & 0xFFFFFFFF)
    return h


def rng_from_seed(seed: int | str) -> np.random.Generator:
    s = _seed_to_uint32(seed)
    return np.random.default_rng(np.uint32(s))


def permutation_table(seed: int | str, n: int = 256) -> np.ndarray:
    rng = rng_from_seed(seed)
    p = np.arange(n, dtype=np.int32)
    rng.shuffle(p)
    return np.concatenate([p, p], axis=0)


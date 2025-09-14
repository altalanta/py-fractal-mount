from __future__ import annotations

import numpy as np

from .perlin import perlin_noise
from .simplex import simplex_noise


def fbm(
    shape: tuple[int, int],
    scale: float,
    perm: np.ndarray,
    octaves: int = 6,
    lacunarity: float = 2.0,
    gain: float = 0.5,
    base: str = "perlin",
) -> np.ndarray:
    h, w = shape
    out = np.zeros((h, w), dtype=np.float32)
    amp = 1.0
    freq = max(scale, 1e-6)
    total_amp = 0.0
    for _ in range(octaves):
        if base == "perlin":
            n = perlin_noise(shape, freq, perm)
        else:
            n = simplex_noise(shape, freq, perm)
        out += n * amp
        total_amp += amp
        freq *= lacunarity
        amp *= gain
    out /= max(total_amp, 1e-8)
    out = (out + 1.0) * 0.5
    return out.astype(np.float32)


def ridged_fbm(
    shape: tuple[int, int],
    scale: float,
    perm: np.ndarray,
    octaves: int = 6,
    lacunarity: float = 2.0,
    gain: float = 0.5,
    sharpness: float = 0.8,
    base: str = "perlin",
) -> np.ndarray:
    h, w = shape
    out = np.zeros((h, w), dtype=np.float32)
    amp = 1.0
    freq = max(scale, 1e-6)
    total_amp = 0.0
    for _ in range(octaves):
        if base == "perlin":
            n = perlin_noise(shape, freq, perm)
        else:
            n = simplex_noise(shape, freq, perm)
        r = 1.0 - np.abs(n)
        r = (r ** (1.0 + sharpness)).astype(np.float32)
        out += r * amp
        total_amp += amp
        freq *= lacunarity
        amp *= gain
    out /= max(total_amp, 1e-8)
    return np.clip(out, 0.0, 1.0)


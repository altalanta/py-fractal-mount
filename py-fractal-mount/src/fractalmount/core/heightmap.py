from __future__ import annotations

import numpy as np

from .params import TerrainParams, NoiseAlgo
from .seed import permutation_table
from .diamond_square import diamond_square
from .noise.fbm import fbm, ridged_fbm
from .domain_warp import domain_warp
from .erosion import hydraulic_erosion
from .post import normalize01, clamp as clamp_fn, terrace as terrace_fn, smooth as smooth_fn


def _apply_island_mask(h: np.ndarray) -> np.ndarray:
    H, W = h.shape
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx = (xx - (W - 1) / 2) / ((W - 1) / 2)
    cy = (yy - (H - 1) / 2) / ((H - 1) / 2)
    r = np.sqrt(cx * cx + cy * cy)
    mask = np.clip(1.0 - r**2, 0.0, 1.0)
    return h * mask


def generate_heightmap(tp: TerrainParams) -> np.ndarray:
    size = tp.size
    perm = permutation_table(tp.seed)
    if tp.algo == NoiseAlgo.DIAMOND_SQUARE:
        base = diamond_square(size, tp.seed, roughness=0.8)
    elif tp.algo == NoiseAlgo.PERLIN_FBM:
        base = fbm((size, size), tp.scale, perm, tp.octaves, tp.lacunarity, tp.gain, base="perlin")
    elif tp.algo == NoiseAlgo.SIMPLEX_FBM:
        base = fbm((size, size), tp.scale, perm, tp.octaves, tp.lacunarity, tp.gain, base="simplex")
    elif tp.algo == NoiseAlgo.RIDGED:
        base = ridged_fbm(
            (size, size), tp.scale, perm, tp.octaves, tp.lacunarity, tp.gain, tp.ridge_sharpness
        )
    else:
        base = domain_warp(
            (size, size), tp.scale, perm, tp.warp_strength, tp.warp_scale, base="perlin"
        )

    h = base
    if tp.island_mask:
        h = _apply_island_mask(h)

    if tp.erosion.iterations > 0:
        h = hydraulic_erosion(
            h,
            iterations=tp.erosion.iterations,
            rain_rate=tp.erosion.rain_rate,
            capacity=tp.erosion.capacity,
            evaporation=tp.erosion.evaporation,
        )

    if tp.post.normalize:
        h = normalize01(h)
    h = clamp_fn(h, tp.post.clamp_min, tp.post.clamp_max)
    h = terrace_fn(h, tp.post.terrace_steps)
    h = smooth_fn(h, tp.post.smooth_kernel)
    h = np.clip(h, 0.0, 1.0).astype(np.float32)
    return h


import numpy as np

from fractalmount.core.params import TerrainParams, NoiseAlgo
from fractalmount.core.heightmap import generate_heightmap


def grad_mag(h: np.ndarray) -> float:
    gx = np.abs(np.diff(h, axis=1)).mean()
    gy = np.abs(np.diff(h, axis=0)).mean()
    return float(gx + gy)


def test_domain_warp_increases_detail():
    base = TerrainParams(seed=5, algo=NoiseAlgo.PERLIN_FBM, size=257)
    warped = TerrainParams(seed=5, algo=NoiseAlgo.WARPED, size=257)
    h0 = generate_heightmap(base)
    h1 = generate_heightmap(warped)
    assert grad_mag(h1) >= 0.9 * grad_mag(h0)


import numpy as np

from fractalmount.core.params import TerrainParams, NoiseAlgo
from fractalmount.core.heightmap import generate_heightmap


def test_heightmap_range_no_nan():
    tp = TerrainParams(seed=42, algo=NoiseAlgo.WARPED, size=257)
    h = generate_heightmap(tp)
    assert np.isfinite(h).all()
    assert h.min() >= 0.0 - 1e-6
    assert h.max() <= 1.0 + 1e-6


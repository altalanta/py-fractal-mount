import numpy as np

from fractalmount.core.params import TerrainParams, NoiseAlgo
from fractalmount.core.heightmap import generate_heightmap


def gradient_magnitude(h: np.ndarray) -> float:
    gx = np.abs(np.diff(h, axis=1)).mean()
    gy = np.abs(np.diff(h, axis=0)).mean()
    return float(gx + gy)


def test_noise_gradients_nonzero():
    for algo in [NoiseAlgo.PERLIN_FBM, NoiseAlgo.SIMPLEX_FBM, NoiseAlgo.RIDGED]:
        tp = TerrainParams(seed=7, algo=algo, size=257)
        h = generate_heightmap(tp)
        g = gradient_magnitude(h)
        assert g > 1e-3


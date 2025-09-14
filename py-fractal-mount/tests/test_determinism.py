import zlib
import numpy as np

from fractalmount.core.params import TerrainParams, NoiseAlgo
from fractalmount.core.heightmap import generate_heightmap
from fractalmount.core.seed import permutation_table


def checksum(a: np.ndarray) -> int:
    return zlib.crc32(a.tobytes())


def test_permutation_deterministic():
    p1 = permutation_table("seed-123")
    p2 = permutation_table("seed-123")
    assert np.array_equal(p1, p2)


def test_heightmap_deterministic():
    tp = TerrainParams(seed="abc", algo=NoiseAlgo.PERLIN_FBM, size=257)
    h1 = generate_heightmap(tp)
    h2 = generate_heightmap(tp)
    assert checksum(h1) == checksum(h2)


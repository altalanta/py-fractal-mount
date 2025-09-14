import numpy as np

from fractalmount.core.mesh import heightmap_to_mesh


def test_mesh_shapes_and_normals():
    size = 17
    hm = np.linspace(0, 1, size * size, dtype=np.float32).reshape(size, size)
    v, f, n = heightmap_to_mesh(hm)
    assert v.shape == (size * size, 3)
    assert f.shape[1] == 3
    expected_tris = 2 * (size - 1) * (size - 1)
    assert f.shape[0] == expected_tris
    assert f.min() >= 0 and f.max() < v.shape[0]
    mag = np.linalg.norm(n, axis=1)
    assert np.allclose(mag, 1.0, atol=1e-3)


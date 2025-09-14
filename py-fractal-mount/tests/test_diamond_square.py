import numpy as np

from fractalmount.core.diamond_square import diamond_square


def test_ds_basic_properties():
    h = diamond_square(257, seed=123, roughness=0.8)
    assert h.shape == (257, 257)
    assert np.isfinite(h).all()
    assert 0.0 - 1e-6 <= h.min() <= 0.1
    assert 0.9 <= h.max() <= 1.0 + 1e-6
    assert h.var() > 1e-4


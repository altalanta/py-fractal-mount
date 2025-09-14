from __future__ import annotations

import numpy as np


def heightmap_to_mesh(hm: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    h, w = hm.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    x = xx / (w - 1)
    y = yy / (h - 1)
    z = hm.astype(np.float32)
    v = np.stack([x, y, z], axis=-1).reshape(-1, 3)

    def vid(i: int, j: int) -> int:
        return i * w + j

    faces = []
    for i in range(h - 1):
        for j in range(w - 1):
            v0 = vid(i, j)
            v1 = vid(i, j + 1)
            v2 = vid(i + 1, j)
            v3 = vid(i + 1, j + 1)
            faces.append([v0, v2, v1])
            faces.append([v2, v3, v1])
    f = np.array(faces, dtype=np.int32)

    n = np.zeros_like(v)
    tri_v0 = v[f[:, 0]]
    tri_v1 = v[f[:, 1]]
    tri_v2 = v[f[:, 2]]
    tri_n = np.cross(tri_v1 - tri_v0, tri_v2 - tri_v0)
    for k in range(f.shape[0]):
        a, b, c = f[k]
        n[a] += tri_n[k]
        n[b] += tri_n[k]
        n[c] += tri_n[k]
    norm = np.linalg.norm(n, axis=1, keepdims=True) + 1e-8
    n = (n / norm).astype(np.float32)
    return v.astype(np.float32), f, n


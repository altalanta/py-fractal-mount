from __future__ import annotations

import numpy as np


def hydraulic_erosion(
    height: np.ndarray,
    iterations: int = 50,
    rain_rate: float = 0.01,
    capacity: float = 1.0,
    evaporation: float = 0.5,
) -> np.ndarray:
    h = height.astype(np.float32).copy()
    water = np.zeros_like(h)
    sediment = np.zeros_like(h)
    H, W = h.shape

    for _ in range(max(0, iterations)):
        water += rain_rate

        dhs = []
        shifts = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1),
        ]
        nh = np.pad(h, ((1, 1), (1, 1)), mode="edge")
        for dy, dx in shifts:
            neigh = nh[1 + dy : 1 + dy + H, 1 + dx : 1 + dx + W]
            dhs.append(neigh - h)
        dh = np.stack(dhs, axis=-1)

        idx = np.argmin(dh, axis=-1)
        min_dh = np.take_along_axis(dh, idx[..., None], axis=-1)[..., 0]
        flow_mask = min_dh < 0.0

        move = np.zeros_like(h)
        move[flow_mask] = np.minimum(water[flow_mask], -min_dh[flow_mask])

        new_water = water.copy()
        new_sed = sediment.copy()
        for k, (dy, dx) in enumerate(shifts):
            mask = flow_mask & (idx == k)
            if not np.any(mask):
                continue
            moved = move * mask
            ratio = sediment / (water + 1e-8)
            new_water -= moved
            new_sed -= moved * ratio * mask

            pad_w = np.pad(new_water, ((1, 1), (1, 1)), mode="edge")
            pad_s = np.pad(new_sed, ((1, 1), (1, 1)), mode="edge")
            pad_w[1 + dy : 1 + dy + H, 1 + dx : 1 + dx + W] += moved
            pad_s[1 + dy : 1 + dy + H, 1 + dx : 1 + dx + W] += moved * ratio * mask
            new_water = pad_w[1:-1, 1:-1]
            new_sed = pad_s[1:-1, 1:-1]

        water = new_water
        sediment = new_sed

        cap = np.maximum(capacity * water, 1e-6)
        over = sediment - cap
        deposit = np.maximum(over, 0.0)
        erode = np.maximum(-over, 0.0)

        h += -deposit + 0.1 * erode
        sediment += -deposit + erode

        water *= 1.0 - evaporation
        water = np.maximum(water, 0.0)

    mn, mx = float(h.min()), float(h.max())
    if mx - mn > 1e-6:
        h = (h - mn) / (mx - mn)
    else:
        h.fill(0.5)
    return h.astype(np.float32)


from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
from PIL import Image


def export_heightmap_png(path: Path | str, hm: np.ndarray, try_16bit: bool = True) -> None:
    p = Path(path)
    hmn = np.clip(hm, 0.0, 1.0).astype(np.float32)
    if try_16bit:
        try:
            arr16 = (hmn * 65535.0 + 0.5).astype(np.uint16)
            img = Image.fromarray(arr16, mode="I;16")
            img.save(p)
            return
        except Exception:
            pass
    arr8 = (hmn * 255.0 + 0.5).astype(np.uint8)
    img = Image.fromarray(arr8, mode="L")
    img.save(p)


def _have_trimesh() -> bool:
    try:  # pragma: no cover - optional
        import trimesh  # noqa: F401
        return True
    except Exception:
        return False


def export_mesh_file(path: Path | str, vertices: np.ndarray, faces: np.ndarray) -> Optional[str]:
    p = Path(path)
    if not _have_trimesh():  # pragma: no cover - optional
        return "trimesh not installed; mesh export disabled"
    import trimesh  # type: ignore  # pragma: no cover - optional

    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    if p.suffix.lower() == ".stl":
        try:
            mesh.export(p)
        except Exception:  # pragma: no cover - optional
            return "numpy-stl not available or STL export failed"
    else:
        mesh.export(p)
    return None


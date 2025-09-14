from __future__ import annotations

import time
from typing import Any, Dict

import numpy as np
from PySide6.QtCore import QThread, Signal

from ..core.heightmap import generate_heightmap
from ..core.params import TerrainParams


class TerrainWorker(QThread):  # pragma: no cover - GUI
    finished_result = Signal(object)

    def __init__(self, params: TerrainParams) -> None:
        super().__init__()
        self._params = params
        self._cancel = False

    def cancel(self) -> None:
        self._cancel = True

    def run(self) -> None:
        t0 = time.perf_counter()
        hm = generate_heightmap(self._params)
        t1 = time.perf_counter()
        if self._cancel:
            return
        res: Dict[str, Any] = {
            "heightmap": hm,
            "min": float(np.min(hm)),
            "max": float(np.max(hm)),
            "timings": {"gen_ms": (t1 - t0) * 1000.0, "erosion_ms": 0.0},
        }
        self.finished_result.emit(res)


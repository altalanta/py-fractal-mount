from __future__ import annotations

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from .controls_panel import ControlsPanel
from .vispy_view import VispyView
from ..workers.terrain_worker import TerrainWorker


class MainWindow(QMainWindow):  # pragma: no cover - GUI
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("FractalMount")
        self.resize(1200, 800)

        central = QWidget(self)
        lay = QHBoxLayout(central)
        self.controls = ControlsPanel(self)
        self.view = VispyView()
        lay.addWidget(self.controls, 0)
        lay.addWidget(self.view.native, 1)
        self.setCentralWidget(central)

        self.controls.params_changed.connect(self.request_generate)
        self.controls.reseed_requested.connect(self.reseed)

        self.worker: TerrainWorker | None = None

        self.request_generate(self.controls.get_params())

    def reseed(self) -> None:
        self.request_generate(self.controls.get_params())

    def request_generate(self, params) -> None:
        if self.worker is not None:
            self.worker.cancel()
        self.worker = TerrainWorker(params)
        self.worker.finished_result.connect(self.on_generated)
        self.worker.start()

    def on_generated(self, result) -> None:
        hm = result["heightmap"]
        self.view.set_heightmap(hm, wireframe=self.controls.get_params().render.wireframe)
        self.controls.set_stats(
            f"Res: {hm.shape[0]} | gen: {result['timings']['gen_ms']:.1f} ms"
        )


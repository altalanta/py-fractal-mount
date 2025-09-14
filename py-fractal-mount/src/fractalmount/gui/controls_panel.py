from __future__ import annotations

from PySide6.QtCore import Signal, QTimer
from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QCheckBox,
    QPushButton,
    QVBoxLayout,
    QLabel,
)

from ..core.params import TerrainParams, NoiseAlgo


class ControlsPanel(QWidget):  # pragma: no cover - GUI
    params_changed = Signal(object)
    reseed_requested = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._timer = QTimer(self)
        self._timer.setInterval(200)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.emit_params)

        self.tp = TerrainParams()
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.algo = QComboBox()
        for a in NoiseAlgo:
            self.algo.addItem(a.value)
        self.algo.setCurrentText(self.tp.algo.value)
        self.algo.currentTextChanged.connect(self._changed)
        form.addRow("Algorithm", self.algo)

        self.seed = QDoubleSpinBox()
        self.seed.setDecimals(0)
        self.seed.setRange(-1e9, 1e9)
        self.seed.setValue(123)
        self.seed.valueChanged.connect(self._changed)
        form.addRow("Seed", self.seed)

        self.size = QComboBox()
        for s in [257, 513, 1025]:
            self.size.addItem(str(s))
        self.size.setCurrentText(str(self.tp.size))
        self.size.currentTextChanged.connect(self._changed)
        form.addRow("Resolution", self.size)

        self.scale = QDoubleSpinBox(); self.scale.setRange(0.01, 100.0); self.scale.setValue(self.tp.scale); self.scale.valueChanged.connect(self._changed)
        form.addRow("Scale", self.scale)
        self.octaves = QSpinBox(); self.octaves.setRange(1, 12); self.octaves.setValue(self.tp.octaves); self.octaves.valueChanged.connect(self._changed)
        form.addRow("Octaves", self.octaves)
        self.lacunarity = QDoubleSpinBox(); self.lacunarity.setRange(1.0, 6.0); self.lacunarity.setSingleStep(0.1); self.lacunarity.setValue(self.tp.lacunarity); self.lacunarity.valueChanged.connect(self._changed)
        form.addRow("Lacunarity", self.lacunarity)
        self.gain = QDoubleSpinBox(); self.gain.setRange(0.0, 1.0); self.gain.setSingleStep(0.05); self.gain.setValue(self.tp.gain); self.gain.valueChanged.connect(self._changed)
        form.addRow("Gain", self.gain)
        self.ridge = QDoubleSpinBox(); self.ridge.setRange(0.0, 2.0); self.ridge.setSingleStep(0.05); self.ridge.setValue(self.tp.ridge_sharpness); self.ridge.valueChanged.connect(self._changed)
        form.addRow("Ridge Sharpness", self.ridge)
        self.warp_strength = QDoubleSpinBox(); self.warp_strength.setRange(0.0, 2.0); self.warp_strength.setSingleStep(0.05); self.warp_strength.setValue(self.tp.warp_strength); self.warp_strength.valueChanged.connect(self._changed)
        form.addRow("Warp Strength", self.warp_strength)
        self.warp_scale = QDoubleSpinBox(); self.warp_scale.setRange(0.1, 10.0); self.warp_scale.setSingleStep(0.1); self.warp_scale.setValue(self.tp.warp_scale); self.warp_scale.valueChanged.connect(self._changed)
        form.addRow("Warp Scale", self.warp_scale)

        self.island = QCheckBox(); self.island.setChecked(self.tp.island_mask); self.island.stateChanged.connect(self._changed)
        form.addRow("Island Mask", self.island)

        layout.addLayout(form)
        self.stats = QLabel("Ready")
        layout.addWidget(self.stats)
        self.reseed = QPushButton("Reseed")
        self.reseed.clicked.connect(self.reseed_requested.emit)
        layout.addWidget(self.reseed)
        layout.addStretch(1)

    def get_params(self) -> TerrainParams:
        return TerrainParams(
            seed=int(self.seed.value()),
            algo=NoiseAlgo(self.algo.currentText()),
            size=int(self.size.currentText()),
            scale=float(self.scale.value()),
            octaves=int(self.octaves.value()),
            lacunarity=float(self.lacunarity.value()),
            gain=float(self.gain.value()),
            ridge_sharpness=float(self.ridge.value()),
            warp_strength=float(self.warp_strength.value()),
            warp_scale=float(self.warp_scale.value()),
            island_mask=bool(self.island.isChecked()),
        )

    def set_stats(self, text: str) -> None:
        self.stats.setText(text)

    def _changed(self, *args) -> None:
        self._timer.start()

    def emit_params(self) -> None:
        self.params_changed.emit(self.get_params())


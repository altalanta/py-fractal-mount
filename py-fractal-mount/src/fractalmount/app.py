from __future__ import annotations

import sys
from typing import Optional


def run(argv: Optional[list[str]] = None) -> int:
    from PySide6.QtWidgets import QApplication
    from .gui.main_window import MainWindow

    app = QApplication(argv or sys.argv)
    win = MainWindow()
    win.show()
    return app.exec()


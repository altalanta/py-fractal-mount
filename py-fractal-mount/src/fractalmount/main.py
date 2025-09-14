from __future__ import annotations

import os
import sys


def main() -> int:
    # Detect headless Linux (no X11/Wayland). macOS/Windows don't need DISPLAY.
    headless = sys.platform.startswith("linux") and (
        os.environ.get("DISPLAY") is None and os.environ.get("WAYLAND_DISPLAY") is None
    )
    if headless:
        print("Headless environment detected (no DISPLAY). Use CLI: `fractalmount --help`.")
        return 0

    try:
        from .app import run
    except Exception as exc:  # pragma: no cover - GUI import errors are not in tests
        print(f"Failed to start GUI: {exc}")
        return 1
    return run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())


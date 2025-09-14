Architecture Overview

- Core algorithms live in `fractalmount.core` and are pure NumPy where possible.
- GUI lives in `fractalmount.gui` with a `VispyView` for the 3D viewport.
- Heavy work runs in `TerrainWorker` (QThread) to keep UI responsive.
- CLI uses the same core generation path and exporters.

Data Flow
- Controls emit `TerrainParams` -> Worker generates heightmap -> View converts to mesh -> display.


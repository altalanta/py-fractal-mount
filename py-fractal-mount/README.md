Fractal Mountain Range Generator (Python, Qt + VisPy)

Features
- Interactive Qt (PySide6) GUI with VisPy 3D viewport
- Deterministic terrain from multiple algorithms: Diamond–Square, Perlin fBm, Simplex fBm, Ridged multifractal, and Domain Warping
- Optional hydraulic erosion pass
- Live parameter editing with background generation (no UI stalls)
- Export heightmap (PNG 8/16-bit) and mesh (OBJ/GLB; STL if numpy-stl present)
- CLI for headless generation
- Tested algorithms with pytest; lint/format via ruff + black

Install
1) Ensure Python 3.11
2) From this folder: `python -m pip install -e .[test]` (zsh users: quote extras like `python -m pip install -e ".[test]"`)

Run
- GUI: `python -m fractalmount`
- CLI: `fractalmount --help`

Performance Tips
- NumPy used throughout; optional numba can accelerate kernels if installed.
- For 513x513, generation is interactive; erosion is slower (documented).
- Headless Linux auto-disables GUI; macOS/Windows launch normally.

Algorithms Overview
- Diamond–Square: midpoint displacement with roughness decay.
- Perlin/Simplex fBm: fractal Brownian motion combining octaves of gradient noise.
- Ridged multifractal: 1 - |noise| combined across octaves.
- Domain warping: two-stage warp at different scales.
- Erosion: simple rain + flow-to-lowest + sediment capacity + evaporation.

License
MIT


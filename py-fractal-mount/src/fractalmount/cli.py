from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Optional

import numpy as np

from .core.heightmap import generate_heightmap
from .core.mesh import heightmap_to_mesh
from .core.params import NoiseAlgo, PostProcessParams, ErosionParams, RenderParams, TerrainParams
from .gui.exporters import export_heightmap_png, export_mesh_file


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Fractal mountain generator (headless)")
    p.add_argument("--seed", type=str, default="123", help="Deterministic seed")
    p.add_argument("--algo", type=str, default="warped",
                   choices=[a.value for a in NoiseAlgo], help="Algorithm")
    p.add_argument("--size", type=int, default=513, choices=[257, 513, 1025], help="Resolution")
    p.add_argument("--scale", type=float, default=1.0, help="Horizontal scale")
    p.add_argument("--octaves", type=int, default=6)
    p.add_argument("--lacunarity", type=float, default=2.0)
    p.add_argument("--gain", type=float, default=0.5)
    p.add_argument("--ridge-sharpness", type=float, default=0.8)
    p.add_argument("--warp-strength", type=float, default=0.35)
    p.add_argument("--warp-scale", type=float, default=1.3)
    p.add_argument("--island-mask", action="store_true")
    p.add_argument("--erosion-iters", type=int, default=0)
    p.add_argument("--out", type=Path, required=True, help="Output heightmap PNG path")
    p.add_argument("--mesh", type=Path, default=None, help="Optional mesh output path (.obj/.glb/.stl)")
    p.add_argument("--settings", type=Path, default=None, help="Optional JSON settings export path")
    return p


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    tp = TerrainParams(
        seed=args.seed,
        algo=NoiseAlgo(args.algo),
        size=args.size,
        scale=args.scale,
        octaves=args.octaves,
        lacunarity=args.lacunarity,
        gain=args.gain,
        ridge_sharpness=args.ridge_sharpness,
        warp_strength=args.warp_strength,
        warp_scale=args.warp_scale,
        island_mask=args.island_mask,
        post=PostProcessParams(),
        erosion=ErosionParams(iterations=args.erosion_iters),
        render=RenderParams(),
    )

    hm = generate_heightmap(tp)
    export_heightmap_png(args.out, hm)
    print(f"Wrote heightmap: {args.out}")

    if args.settings:
        args.settings.write_text(json.dumps(tp.to_dict(), indent=2))
        print(f"Wrote settings: {args.settings}")

    if args.mesh is not None:
        v, f, n = heightmap_to_mesh(hm)
        export_mesh_file(args.mesh, v, f)
        print(f"Wrote mesh: {args.mesh}")

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())


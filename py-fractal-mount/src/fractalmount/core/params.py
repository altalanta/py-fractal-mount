from __future__ import annotations

from dataclasses import dataclass, asdict, field
from enum import Enum
from typing import Any, Dict


class NoiseAlgo(str, Enum):
    DIAMOND_SQUARE = "diamond_square"
    PERLIN_FBM = "perlin_fbm"
    SIMPLEX_FBM = "simplex_fbm"
    RIDGED = "ridged"
    WARPED = "warped"


@dataclass
class PostProcessParams:
    normalize: bool = True
    clamp_min: float | None = 0.0
    clamp_max: float | None = 1.0
    terrace_steps: int = 0
    smooth_kernel: int = 0


@dataclass
class ErosionParams:
    iterations: int = 0
    rain_rate: float = 0.01
    capacity: float = 1.0
    evaporation: float = 0.5


@dataclass
class RenderParams:
    mode: str = "shaded"
    wireframe: bool = False
    contours: bool = False
    colormap: str = "Alpine"
    view_min: float = 0.0
    view_max: float = 1.0


@dataclass
class TerrainParams:
    seed: int | str = 0
    algo: NoiseAlgo = NoiseAlgo.WARPED
    size: int = 513
    scale: float = 1.0
    octaves: int = 6
    lacunarity: float = 2.0
    gain: float = 0.5
    ridge_sharpness: float = 0.8
    warp_strength: float = 0.35
    warp_scale: float = 1.3
    island_mask: bool = False
    post: PostProcessParams = field(default_factory=PostProcessParams)
    erosion: ErosionParams = field(default_factory=ErosionParams)
    render: RenderParams = field(default_factory=RenderParams)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["algo"] = self.algo.value
        return d


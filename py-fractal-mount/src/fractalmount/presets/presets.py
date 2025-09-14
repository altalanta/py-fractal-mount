from __future__ import annotations

from ..core.params import TerrainParams, NoiseAlgo, PostProcessParams, ErosionParams, RenderParams


def alpine_preset() -> TerrainParams:
    return TerrainParams(
        seed=123,
        algo=NoiseAlgo.WARPED,
        size=513,
        scale=1.0,
        octaves=6,
        lacunarity=2.0,
        gain=0.5,
        ridge_sharpness=0.8,
        warp_strength=0.35,
        warp_scale=1.3,
        island_mask=False,
        post=PostProcessParams(normalize=True, clamp_min=0.0, clamp_max=1.0, terrace_steps=0, smooth_kernel=0),
        erosion=ErosionParams(iterations=0),
        render=RenderParams(colormap="Alpine"),
    )


def desert_preset() -> TerrainParams:
    return TerrainParams(
        seed=777,
        algo=NoiseAlgo.RIDGED,
        size=513,
        scale=0.8,
        octaves=5,
        lacunarity=2.2,
        gain=0.55,
        ridge_sharpness=1.1,
        warp_strength=0.2,
        warp_scale=1.1,
        island_mask=False,
        post=PostProcessParams(normalize=True, clamp_min=0.0, clamp_max=1.0, terrace_steps=6, smooth_kernel=3),
        erosion=ErosionParams(iterations=0),
        render=RenderParams(colormap="Desert"),
    )


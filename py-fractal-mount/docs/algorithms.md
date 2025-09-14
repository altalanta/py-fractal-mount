Algorithms Summary

Diamond–Square
- Classic midpoint displacement; roughness decays each level; edges clamped.

Gradient Noise (Perlin & Simplex)
- Vectorized 2D implementations; fBm combines octaves with lacunarity/gain.

Ridged Multifractal
- Uses 1 - |noise| basis; sharpness controls ridge shaping; normalized to [0,1].

Domain Warping
- Two-stage warp using gradient noise fields added to coordinates.

Hydraulic Erosion (Simple)
- Cellular approximation: rain, flow-to-lowest neighbor, sediment carry/capacity, evaporation.


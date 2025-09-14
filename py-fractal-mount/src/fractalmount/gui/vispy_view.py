from __future__ import annotations

import numpy as np

from vispy import scene
from vispy.scene import visuals

from ..core.mesh import heightmap_to_mesh


class VispyView(scene.SceneCanvas):  # pragma: no cover - GUI
    def __init__(self) -> None:
        super().__init__(keys=None, size=(800, 600), bgcolor="black")
        self.unfreeze()
        self.view = self.central_widget.add_view()
        self.view.camera = scene.cameras.TurntableCamera(fov=45.0, up="z")
        self.mesh_visual = visuals.Mesh(shading="smooth")
        self.wire_visual = visuals.MeshWireframe()
        self.view.add(self.mesh_visual)
        self.view.add(self.wire_visual)
        self.wire_visual.visible = False
        self.freeze()

    def set_heightmap(self, hm: np.ndarray, wireframe: bool = False) -> None:
        v, f, n = heightmap_to_mesh(hm)
        self.mesh_visual.set_data(vertices=v, faces=f, vertex_normals=n, color=(0.7, 0.7, 0.8, 1.0))
        self.wire_visual.set_data(vertices=v, faces=f)
        self.wire_visual.visible = wireframe
        self._frame_bbox(v)

    def toggle_wireframe(self, show: bool) -> None:
        self.wire_visual.visible = show
        self.update()

    def _frame_bbox(self, v: np.ndarray) -> None:
        mins = v.min(axis=0)
        maxs = v.max(axis=0)
        center = 0.5 * (mins + maxs)
        size = max(maxs - mins)
        self.view.camera.center = center
        self.view.camera.scale_factor = size


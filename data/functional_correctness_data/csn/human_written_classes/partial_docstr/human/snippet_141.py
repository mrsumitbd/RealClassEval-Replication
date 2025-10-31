import numpy as np

class _EmbreeWrap:
    """
    A light wrapper for Embreex scene objects which
    allows queries to be scaled to help with precision
    issues, as well as selecting the correct dtypes.
    """

    def __init__(self, vertices, faces, scale):
        scaled = np.array(vertices, dtype=np.float64)
        self.origin = scaled.min(axis=0)
        self.scale = float(scale)
        scaled = (scaled - self.origin) * self.scale
        self.scene = rtcore_scene.EmbreeScene()
        TriangleMesh(scene=self.scene, vertices=scaled.astype(_embree_dtype), indices=faces.view(np.ndarray).astype(np.int32))

    def run(self, origins, normals, **kwargs):
        scaled = (np.array(origins, dtype=np.float64) - self.origin) * self.scale
        return self.scene.run(scaled.astype(_embree_dtype), normals.astype(_embree_dtype), **kwargs)
class Mesh:

    def __init__(self, data):
        """Constructor.

        Args:
            data (tuple[raw_volume, mesh]): tuple containing the raw data and the mesh data
        """
        self._raw_vol = data[0]
        self._mesh = data[1]

    def ng_mesh(self):
        """Convert mesh to precompute format for Neuroglancer visualization

        Args:
            mesh: mesh to convert.

        Returns:
            (): Returns mesh precompute format

        """
        return self._mesh.to_precomputed()

    def obj_mesh(self):
        """Convert mesh to obj

        Args:
            mesh: mesh to convert.

        Returns:
            (): Returns mesh obj format

        """
        return self._mesh.to_obj()
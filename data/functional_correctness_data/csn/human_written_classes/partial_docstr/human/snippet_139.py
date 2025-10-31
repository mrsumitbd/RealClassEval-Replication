class Permutator:

    def __init__(self, mesh):
        """
        A convenience object to get permutated versions of a mesh.
        """
        self._mesh = mesh

    def transform(self, translation_scale=1000):
        return transform(self._mesh, translation_scale=translation_scale)

    def noise(self, magnitude=None):
        return noise(self._mesh, magnitude)

    def tessellation(self):
        return tessellation(self._mesh)
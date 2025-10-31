class Mesh:
    """This is a basic mesh for drawing using OpenGL. Interestingly, it does
    not contain its own vertices. These are instead drawn via materials."""

    def __init__(self, name=None, has_faces=False):
        self.name = name
        self.materials = []
        self.has_faces = has_faces
        self.faces = []

    def has_material(self, new_material):
        """Determine whether we already have a material of this name."""
        for material in self.materials:
            if material.name == new_material.name:
                return True
        return False

    def add_material(self, material):
        """Add a material to the mesh, IF it's not already present."""
        if self.has_material(material):
            return
        self.materials.append(material)
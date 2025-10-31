import gmsh

class SetBackgroundMesh:

    def __init__(self, fields, operator):
        self.fields = fields
        self.operator = operator

    def exec(self):
        tag = gmsh.model.mesh.field.add(self.operator)
        gmsh.model.mesh.field.setNumbers(tag, 'FieldsList', [f.tag for f in self.fields])
        gmsh.model.mesh.field.setAsBackgroundMesh(tag)
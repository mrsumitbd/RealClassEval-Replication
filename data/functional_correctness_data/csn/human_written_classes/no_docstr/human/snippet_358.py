import gmsh

class BoundaryLayer:

    def __init__(self, lcmin, lcmax, distmin, distmax, edges_list=None, faces_list=None, nodes_list=None, num_points_per_curve=None):
        self.lcmin = lcmin
        self.lcmax = lcmax
        self.distmin = distmin
        self.distmax = distmax
        self.edges_list = edges_list or []
        self.faces_list = faces_list or []
        self.nodes_list = nodes_list or []
        self.num_points_per_curve = num_points_per_curve

    def exec(self):
        tag1 = gmsh.model.mesh.field.add('Distance')
        if self.edges_list:
            gmsh.model.mesh.field.setNumbers(tag1, 'EdgesList', [e._id for e in self.edges_list])
        if self.faces_list:
            gmsh.model.mesh.field.setNumbers(tag1, 'FacesList', [f._id for f in self.faces_list])
        if self.nodes_list:
            gmsh.model.mesh.field.setNumbers(tag1, 'NodesList', [n._id for n in self.nodes_list])
        if self.num_points_per_curve:
            gmsh.model.mesh.field.setNumber(tag1, 'NumPointsPerCurve', self.num_points_per_curve)
        tag2 = gmsh.model.mesh.field.add('Threshold')
        gmsh.model.mesh.field.setNumber(tag2, 'IField', tag1)
        gmsh.model.mesh.field.setNumber(tag2, 'LcMin', self.lcmin)
        gmsh.model.mesh.field.setNumber(tag2, 'LcMax', self.lcmax)
        gmsh.model.mesh.field.setNumber(tag2, 'DistMin', self.distmin)
        gmsh.model.mesh.field.setNumber(tag2, 'DistMax', self.distmax)
        self.tag = tag2
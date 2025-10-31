class OBJMesh:

    def __init__(self, mesh):
        if mesh.mesh_compression:
            raise NotImplementedError('(%s) compressed meshes are not supported' % mesh.name)
        self.mesh_data = MeshData(mesh)
        self.mesh = mesh

    @staticmethod
    def face_str(indices, coords, normals):
        ret = ['f ']
        for i in indices[::-1]:
            ret.append(str(i + 1))
            if coords or normals:
                ret.append('/')
                if coords:
                    ret.append(str(i + 1))
                if normals:
                    ret.append('/')
                    ret.append(str(i + 1))
            ret.append(' ')
        ret.append('\n')
        return ''.join(ret)

    def export(self):
        ret = []
        verts_per_face = 3
        normals = self.mesh_data.normals
        tex_coords = self.mesh_data.uv1
        if not tex_coords:
            tex_coords = self.mesh_data.uv2
        for v in self.mesh_data.vertices:
            ret.append('v %s\n' % v)
        for v in normals:
            ret.append('vn %s\n' % v)
        for v in tex_coords:
            ret.append('vt %s\n' % v)
        ret.append('\n')
        ret.append('g %s\n' % self.mesh.name)
        ret.append('s 1\n')
        sub_count = len(self.mesh.submeshes)
        for i in range(0, sub_count):
            if sub_count == 1:
                ret.append('usemtl %s\n' % self.mesh.name)
            else:
                ret.append('usemtl %s_%d\n' % (self.mesh.name, i))
            face_tri = []
            for t in self.mesh_data.triangles[i]:
                face_tri.append(t)
                if len(face_tri) == verts_per_face:
                    ret.append(self.face_str(face_tri, tex_coords, normals))
                    face_tri = []
            ret.append('\n')
        return ''.join(ret)
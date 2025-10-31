import open3d as o3d
from stl import mesh
import os
import numpy as np
import pymeshlab
import logging

class MeshFormatTransition:

    def __init__(self, case_path, save_path, caseID, compute_closest_point=False):
        self.case_path = case_path
        self.save_path = save_path
        self.caseID = caseID
        self.compute_closest_point = compute_closest_point

    def combine_stl(self):
        stl_files = [f for f in os.listdir(self.case_path) if f[-4:] == '.stl']
        combined_meshes = None
        for stl_file in stl_files:
            current_mesh = mesh.Mesh.from_file(self.case_path + stl_file)
            if combined_meshes is None:
                combined_meshes = current_mesh.data.copy()
            else:
                combined_meshes = np.concatenate([combined_meshes, current_mesh.data])
        combined_mesh = mesh.Mesh(combined_meshes)
        combined_mesh.save(self.case_path + f'/{self.caseID[5:]}.stl')

    def refine_stl(self):
        mesh = pymeshlab.MeshSet()
        mesh.load_new_mesh(self.case_path + f'/{self.caseID[5:]}.stl')
        mesh.apply_filter('meshing_isotropic_explicit_remeshing', iterations=5, targetlen=pymeshlab.PercentageValue(0.03))
        logging.info('Refined TriangleMesh with %s points and %s triangles.' % (mesh.current_mesh().vertex_number(), mesh.current_mesh().face_number()))
        mesh.save_current_mesh(self.case_path + f'/{self.caseID[5:]}_refined.stl')

    def mesh_stl_to_ply(self, doCombine=False, doRefine=False):
        if doCombine:
            self.combine_stl()
        if doRefine:
            self.refine_stl()
        stl_mesh = o3d.io.read_triangle_mesh(self.case_path + f'/{self.caseID[5:]}.stl')
        logging.info(stl_mesh)
        stl_mesh.compute_vertex_normals()
        o3d.io.write_triangle_mesh(self.save_path + f'/mesh_{self.caseID[:4].zfill(4)}.ply', stl_mesh)
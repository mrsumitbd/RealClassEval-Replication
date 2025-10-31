import json
import numpy as np
import os
import open3d as o3d

class Compute_df_stl:

    def __init__(self, geo_path, save_path, stlID, index, bounds_dir):
        self.geo_path = geo_path
        self.save_path = save_path
        self.stlID = stlID
        self.bounds_dir = bounds_dir
        self.query_points = self.compute_query_points()
        self.index = index

    def compute_query_points(self, eps=1e-06):
        with open(os.path.join(self.bounds_dir, 'global_bounds.txt'), 'r') as fp:
            min_bounds = fp.readline().split(' ')
            max_bounds = fp.readline().split(' ')
            min_bounds = [float(a) - eps for a in min_bounds]
            max_bounds = [float(a) + eps for a in max_bounds]
        sdf_spatial_resolution = [64, 64, 64]
        tx = np.linspace(min_bounds[0], max_bounds[0], sdf_spatial_resolution[0])
        ty = np.linspace(min_bounds[1], max_bounds[1], sdf_spatial_resolution[1])
        tz = np.linspace(min_bounds[2], max_bounds[2], sdf_spatial_resolution[2])
        query_points = np.stack(np.meshgrid(tx, ty, tz, indexing='ij'), axis=-1).astype(np.float32)
        return query_points

    def compute_df_from_mesh(self):
        stl_mesh = o3d.io.read_triangle_mesh(os.path.join(self.geo_path, self.stlID))
        num_triangles = len(stl_mesh.triangles)
        print(f'Mesh num in stl: {num_triangles}')
        json_file_path = os.path.join(self.save_path, self.stlID[:-4] + '_mesh_num.json')
        os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
        if os.path.isfile(json_file_path):
            os.remove(json_file_path)
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump({'surface_mesh_num': num_triangles}, file)
        o3d_mesh = o3d.t.geometry.TriangleMesh.from_legacy(stl_mesh)
        scene = o3d.t.geometry.RaycastingScene()
        _ = scene.add_triangles(o3d_mesh)
        df = scene.compute_distance(o3d.core.Tensor(self.query_points)).numpy()
        df_dict = {'df': df}
        np.save(f'{self.save_path}/df_{str(self.index).zfill(4)}.npy', df_dict['df'])
        print(f"df has been saved to : {os.path.join(self.save_path, f'df_{str(self.index).zfill(4)}.npy')}")
        return None
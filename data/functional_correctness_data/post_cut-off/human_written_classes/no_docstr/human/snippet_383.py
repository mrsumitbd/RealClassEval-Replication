import numpy as np
import open3d as o3d
import os

class ComputeDF:

    def __init__(self, case_path, save_path, caseID, geo='mesh'):
        self.case_path = case_path
        self.save_path = save_path
        self.caseID = caseID
        self.query_points = self.compute_query_points()
        self.geo = geo

    def compute_query_points(self, eps=1e-06):
        with open(os.path.join(self.save_path, 'global_bounds.txt'), 'r') as fp:
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
        stl_mesh = o3d.io.read_triangle_mesh(self.case_path + f'/{self.caseID[5:]}.stl')
        stl_mesh = o3d.t.geometry.TriangleMesh.from_legacy(stl_mesh)
        scene = o3d.t.geometry.RaycastingScene()
        _ = scene.add_triangles(stl_mesh)
        df = scene.compute_distance(o3d.core.Tensor(self.query_points)).numpy()
        closest_point = scene.compute_closest_points(o3d.core.Tensor(self.query_points))['points'].numpy()
        df_dict = {'df': df}
        return df_dict

    def compute_df_from_pcd(self):
        query_points = self.query_points.reshape(-1, 3)
        query_points = o3d.utility.Vector3dVector(query_points)
        pcd_query_points = o3d.geometry.PointCloud()
        pcd_query_points.points = query_points
        train_point = np.load(os.path.join(self.case_path, f'centroid_{self.caseID[:4].zfill(4)}.npy'))
        train_point = o3d.utility.Vector3dVector(train_point)
        pcd_train = o3d.geometry.PointCloud()
        pcd_train.points = train_point
        df = pcd_query_points.compute_point_cloud_distance(pcd_train)
        df = np.asarray(df).reshape(64, 64, 64)
        closest_point = None
        df_dict = {'df': df}
        return df_dict

    def save_df(self):
        if self.geo == 'mesh':
            df_dict = self.compute_df_from_mesh()
        elif self.geo == 'pcd':
            df_dict = self.compute_df_from_pcd()
        else:
            raise 'Not supported geometry source. Only Mesh or PCD supported.'
        np.save(os.path.join(self.save_path, f'df_{self.caseID[:4].zfill(4)}.npy'), df_dict['df'])
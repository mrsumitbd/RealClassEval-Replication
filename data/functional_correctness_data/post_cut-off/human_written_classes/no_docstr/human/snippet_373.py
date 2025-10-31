import numpy as np
import os
from stl import mesh
import paddle

class STLConvert:

    def __init__(self, geo_path, save_path, stpID, index, info):
        self.geo_path = geo_path
        self.save_path = save_path
        self.stpID = stpID
        self.info = info
        self.index = index

    def extract_values_from_arrays(self):
        stlID = f'{self.stpID[:-4]}.stl'
        stl_mesh = mesh.Mesh.from_file(os.path.join(self.geo_path, stlID))
        normals = stl_mesh.normals
        unit_normals = -1 * normals / np.linalg.norm(normals, axis=1, keepdims=True)
        vertices = stl_mesh.points.reshape(-1, 3, 3)
        centroid = vertices.mean(axis=1)
        v0, v1, v2 = (vertices[:, 0], vertices[:, 1], vertices[:, 2])
        vec1 = v1 - v0
        vec2 = v2 - v0
        cross_product = np.cross(vec1, vec2)
        areas = np.linalg.norm(cross_product, axis=1) / 2
        print('stl cell number:', len(centroid))
        print('centroid:', centroid, '\n', 'areas:', areas, '\n', 'normals:', unit_normals)
        print(f'area, centrods, normal has been saved to : {self.save_path}')
        os.makedirs(self.save_path, exist_ok=True)
        np.save(f'{self.save_path}/area_{str(self.index).zfill(4)}.npy', areas.astype(np.float32))
        np.save(f'{self.save_path}/centroid_{str(self.index).zfill(4)}.npy', centroid.astype(np.float32))
        np.save(f'{self.save_path}/normal_{str(self.index).zfill(4)}.npy', unit_normals.astype(np.float32))
        print('Mesh information extracted and saved as NumPy arrays.')

    def save_info(self):
        paddle.save(obj=self.info, path=f'{self.save_path}/info_{str(self.index).zfill(4)}.pdparams')
        print(f"info has been saved to : {f'{self.save_path}/info_{str(self.index).zfill(4)}.pdparams'}")
        return None
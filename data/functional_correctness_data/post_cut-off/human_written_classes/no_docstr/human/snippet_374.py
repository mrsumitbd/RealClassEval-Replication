import paddle
import pandas as pd
import numpy as np
import os

class CSVConvert:

    def __init__(self, mesh_path, save_path, csvID, index, info):
        self.csv_data = pd.read_csv(os.path.join(mesh_path, csvID)).to_numpy()
        self.centroid = self.csv_data[:, -3:]
        self.cell_area_ijk = self.csv_data[:, :3]
        self.inward_surface_normal = None
        self.cell_area = None
        self.mesh_path = mesh_path
        self.save_path = save_path
        self.csvID = csvID
        self.info = info
        self.index = index

    @property
    def area(self):
        try:
            self.cell_area = np.sqrt(np.sum(self.cell_area_ijk ** 2, axis=1))
        except TypeError:
            print(f'{self.csvID} skipped.')
        return self.cell_area

    @property
    def normal(self):
        self.inward_surface_normal = -1 * self.cell_area_ijk / self.cell_area[:, np.newaxis]
        return self.inward_surface_normal

    def save_volume_mesh(self):
        print('csv cell number:', len(self.centroid))
        print(f'area, centroids, normal are saving to : {self.save_path}')
        os.makedirs(self.save_path, exist_ok=True)
        np.save(f'{self.save_path}/area_{str(self.index).zfill(4)}.npy', self.area.astype(np.float32))
        np.save(f'{self.save_path}/centroid_{str(self.index).zfill(4)}.npy', self.centroid.astype(np.float32))
        np.save(f'{self.save_path}/normal_{str(self.index).zfill(4)}.npy', self.inward_surface_normal.astype(np.float32))
        print('Volume mesh information has been saved as NumPy arrays.')
        return None

    def save_info(self):
        paddle.save(obj=self.info, path=f'{self.save_path}/info_{str(self.index).zfill(4)}.pdparams')
        print(f"info has been saved to : {os.path.join(self.save_path, f'info_{str(self.index).zfill(4)}.pdparams')}")
        return None
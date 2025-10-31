
import os
import subprocess
from pathlib import Path


class _TPCDataGenerator:

    def __init__(self, scale_factor: int, target_mount_folder_path: str = None, target_row_group_size_mb: int = 128):
        self.scale_factor = scale_factor
        self.target_mount_folder_path = target_mount_folder_path
        self.target_row_group_size_mb = target_row_group_size_mb
        self.tpc_ds_path = Path(__file__).parent / 'tpcds-kit'
        self.data_path = Path(target_mount_folder_path or os.getcwd()) / 'data'
        self.data_path.mkdir(parents=True, exist_ok=True)

    def run(self):
        self._generate_data()
        self._convert_to_parquet()

    def _generate_data(self):
        command = f'{self.tpc_ds_path}/tools/dsdgen -scale {self.scale_factor} -dir {self.data_path}'
        subprocess.run(command, shell=True, check=True)

    def _convert_to_parquet(self):
        command = f'{self.tpc_ds_path}/tools/tpcds2parquet {self.data_path} {self.data_path} {self.target_row_group_size_mb}'
        subprocess.run(command, shell=True, check=True)

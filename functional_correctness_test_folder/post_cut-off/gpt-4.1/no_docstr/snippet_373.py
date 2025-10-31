
import os
import random
import string


class _TPCDataGenerator:

    def __init__(self, scale_factor: int, target_mount_folder_path: str = None, target_row_group_size_mb: int = 128):
        self.scale_factor = scale_factor
        self.target_mount_folder_path = target_mount_folder_path or os.getcwd()
        self.target_row_group_size_mb = target_row_group_size_mb
        self.data_file = os.path.join(
            self.target_mount_folder_path, f"tpc_data_sf{self.scale_factor}.csv")
        self.rows_per_mb = 1000  # Simulated: 1000 rows per MB

    def _generate_row(self):
        # Simulate a row with random data
        id_val = random.randint(1, 1000000)
        name = ''.join(random.choices(string.ascii_letters, k=10))
        value = round(random.uniform(1, 10000), 2)
        return f"{id_val},{name},{value}\n"

    def run(self):
        total_rows = self.scale_factor * self.target_row_group_size_mb * self.rows_per_mb
        os.makedirs(self.target_mount_folder_path, exist_ok=True)
        with open(self.data_file, "w") as f:
            f.write("id,name,value\n")
            for _ in range(total_rows):
                f.write(self._generate_row())

import json
import math
import os
import time
from pathlib import Path


class _TPCDataGenerator:

    def __init__(self, scale_factor: int, target_mount_folder_path: str = None, target_row_group_size_mb: int = 128):
        if not isinstance(scale_factor, int):
            raise TypeError("scale_factor must be an int")
        if scale_factor <= 0:
            raise ValueError("scale_factor must be a positive integer")
        if not isinstance(target_row_group_size_mb, int):
            raise TypeError("target_row_group_size_mb must be an int")
        if target_row_group_size_mb <= 0:
            raise ValueError(
                "target_row_group_size_mb must be a positive integer")

        self.scale_factor = scale_factor
        self.target_row_group_size_mb = target_row_group_size_mb

        base_dir = Path(
            target_mount_folder_path) if target_mount_folder_path else Path.cwd()
        base_dir = base_dir.expanduser().resolve()

        if not base_dir.exists():
            base_dir.mkdir(parents=True, exist_ok=True)

        dataset_base_name = f"tpc_data_sf{self.scale_factor}_rgs{self.target_row_group_size_mb}"
        candidate_path = base_dir / dataset_base_name

        if candidate_path.exists() and any(candidate_path.iterdir()):
            suffix = 1
            while True:
                alt = base_dir / f"{dataset_base_name}_{suffix}"
                if not alt.exists():
                    candidate_path = alt
                    break
                suffix += 1

        self.output_path = candidate_path

    def run(self):
        self.output_path.mkdir(parents=True, exist_ok=True)
        data_dir = self.output_path / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        total_size_mb = self.scale_factor * 1000
        num_row_groups = max(1, math.ceil(
            total_size_mb / self.target_row_group_size_mb))

        for i in range(num_row_groups):
            fpath = data_dir / f"rg-{i:05d}.parquet"
            # Placeholder small content to avoid heavy disk usage
            with open(fpath, "wb") as f:
                f.write(
                    (
                        "PARQUET_PLACEHOLDER\n"
                        f"row_group_index={i}\n"
                        f"scale_factor={self.scale_factor}\n"
                        f"target_row_group_size_mb={self.target_row_group_size_mb}\n"
                    ).encode("utf-8")
                )

        manifest = {
            "created_at_epoch": int(time.time()),
            "output_path": str(self.output_path),
            "data_dir": str(data_dir),
            "scale_factor": self.scale_factor,
            "target_row_group_size_mb": self.target_row_group_size_mb,
            "estimated_total_size_mb": total_size_mb,
            "row_groups": num_row_groups,
            "files": [f"rg-{i:05d}.parquet" for i in range(num_row_groups)],
        }
        with open(self.output_path / "manifest.json", "w", encoding="utf-8") as mf:
            json.dump(manifest, mf, indent=2)

        return {
            "output_path": str(self.output_path),
            "data_dir": str(data_dir),
            "row_groups": num_row_groups,
            "estimated_total_size_mb": total_size_mb,
        }

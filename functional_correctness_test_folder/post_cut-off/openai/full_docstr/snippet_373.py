
import os
import shutil
import tempfile
import math
from pathlib import Path
from typing import Dict

import duckdb
import pandas as pd


class _TPCDataGenerator:
    """
    Base class for TPC data generation. PLEASE DO NOT INSTANTIATE THIS CLASS DIRECTLY.
    Use the TPCHDataGenerator and TPCDSDataGenerator subclasses instead.
    """

    def __init__(self, scale_factor: int, target_mount_folder_path: str = None,
                 target_row_group_size_mb: int = 128):
        """
        Initialize the TPC data generator with a scale factor.

        Parameters
        ----------
        scale_factor : int
            The scale factor for the data generation.
        target_mount_folder_path : str, optional
            Path to the folder where Parquet files will be written.
            If None, a temporary directory will be created and removed after run().
        target_row_group_size_mb : int, default 128
            Desired row group size in megabytes for the output Parquet files.
        """
        if not isinstance(scale_factor, int):
            raise TypeError("scale_factor must be an integer")
        if scale_factor <= 0:
            raise ValueError("scale_factor must be positive")

        if target_row_group_size_mb is None:
            target_row_group_size_mb = 128
        if not isinstance(target_row_group_size_mb, int):
            raise TypeError("target_row_group_size_mb must be an integer")
        if target_row_group_size_mb <= 0:
            raise ValueError("target_row_group_size_mb must be positive")

        self.scale_factor = scale_factor
        self.target_row_group_size_mb = target_row_group_size_mb

        if target_mount_folder_path is None:
            self.target_mount_folder_path = Path(
                tempfile.mkdtemp(prefix="tpc_data_"))
            self._temp_dir_created = True
        else:
            self.target_mount_folder_path = Path(target_mount_folder_path

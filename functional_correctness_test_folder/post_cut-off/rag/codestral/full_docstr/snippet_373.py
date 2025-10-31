
import duckdb
import os
import shutil
from typing import Dict, List, Optional


class _TPCDataGenerator:
    '''
    Base class for TPC data generation. PLEASE DO NOT INSTANTIATE THIS CLASS DIRECTLY. Use the TPCHDataGenerator and TPCDSDataGenerator
    subclasses instead.
    '''

    def __init__(self, scale_factor: int, target_mount_folder_path: str = None, target_row_group_size_mb: int = 128):
        '''
        Initialize the TPC data generator with a scale factor.
        :param scale_factor: The scale factor for the data generation.
        '''
        self.scale_factor = scale_factor
        self.target_mount_folder_path = target_mount_folder_path
        self.target_row_group_size_mb = target_row_group_size_mb
        self.conn = duckdb.connect()
        self.tables: List[str] = []
        self.table_sizes: Dict[str, int] = {}

    def run(self):
        '''
        This method uses DuckDB to generate in-memory tables based on the specified
        scale factor and writes them to Parquet files. It estimates the average row
        size in MB using a sample of the data since DuckDB only supports specifying
        the number of rows per row group. The generated tables are written to the
        specified target folder with optimized row group sizes.
        Parameters
        ----------
        None
        Notes
        -----
        - The method creates a sample Parquet file for each table to estimate row sizes.
        - The full table is then written as Parquet files with optimized row group sizes.
        - Temporary files and in-memory tables are cleaned up after processing.
        '''
        if not self.tables:
            raise ValueError("No tables defined for generation.")

        if self.target_mount_folder_path and not os.path.exists(self.target_mount_folder_path):
            os.makedirs(self.target_mount_folder_path)

        temp_dir = os.path.join(self.target_mount_folder_path,
                                "temp") if self.target_mount_folder_path else "temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        try:
            for table in self.tables:
                # Generate sample data to estimate row size
                sample_query = f"SELECT * FROM {table} LIMIT 1000"
                sample_path = os.path.join(temp_dir, f"{table}_sample.parquet")
                self.conn.execute(
                    f"COPY ({sample_query}) TO '{sample_path}' (FORMAT PARQUET)")

                # Calculate average row size
                sample_size = os.path.getsize(
                    sample_path) / (1024 * 1024)  # in MB
                avg_row_size = sample_size / 1000  # assuming 1000 rows in sample

                # Calculate rows per row group
                rows_per_row_group = int(
                    self.target_row_group_size_mb / avg_row_size)

                # Generate full data with optimized row group size
                full_path = os.path.join(
                    self.target_mount_folder_path, f"{table}.parquet") if self.target_mount_folder_path else f"{table}.parquet"
                self.conn.execute(
                    f"COPY (SELECT * FROM {table}) TO '{full_path}' (FORMAT PARQUET, ROW_GROUP_SIZE {rows_per_row_group})")

                # Store table size
                self.table_sizes[table] = os.path.getsize(full_path)

        finally:
            # Clean up temporary files
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

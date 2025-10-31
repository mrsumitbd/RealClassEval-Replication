
import duckdb
import os
import shutil
import tempfile
from typing import Optional


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
        self.temp_dir = tempfile.mkdtemp()
        self.tables = []

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
            raise ValueError(
                "No tables defined for generation. Subclasses must populate self.tables list.")

        for table_name in self.tables:
            # Generate sample data to estimate row size
            sample_query = f"SELECT * FROM {table_name}({self.scale_factor}) LIMIT 1000"
            sample_path = os.path.join(
                self.temp_dir, f"{table_name}_sample.parquet")
            self.conn.execute(
                f"COPY ({sample_query}) TO '{sample_path}' (FORMAT PARQUET)")

            # Get sample file size to estimate row size
            sample_size_mb = os.path.getsize(sample_path) / (1024 * 1024)
            avg_row_size_mb = sample_size_mb / 1000
            rows_per_group = int(
                self.target_row_group_size_mb / avg_row_size_mb)

            # Generate full table with optimized row group size
            full_query = f"SELECT * FROM {table_name}({self.scale_factor})"
            output_path = os.path.join(
                self.target_mount_folder_path or self.temp_dir, f"{table_name}.parquet")
            self.conn.execute(
                f"COPY ({full_query}) TO '{output_path}' (FORMAT PARQUET, ROW_GROUP_SIZE {rows_per_group})")

            # Clean up sample file
            os.remove(sample_path)

        # Clean up connection
        self.conn.close()

        # If no target folder specified, keep files in temp dir (caller must handle cleanup)
        if not self.target_mount_folder_path:
            print(
                f"Generated files stored in temporary directory: {self.temp_dir}")

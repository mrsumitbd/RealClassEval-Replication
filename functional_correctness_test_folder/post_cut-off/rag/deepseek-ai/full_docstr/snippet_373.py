
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
        :param target_mount_folder_path: The target folder path for the generated Parquet files.
        :param target_row_group_size_mb: The target row group size in MB.
        '''
        self.scale_factor = scale_factor
        self.target_mount_folder_path = target_mount_folder_path
        self.target_row_group_size_mb = target_row_group_size_mb
        self.temp_dir = tempfile.mkdtemp()
        self.conn = duckdb.connect()

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
        if not self.target_mount_folder_path:
            raise ValueError("Target mount folder path must be specified.")

        os.makedirs(self.target_mount_folder_path, exist_ok=True)

        # Generate tables (implemented in subclasses)
        tables = self._generate_tables()

        for table_name, query in tables.items():
            # Create a sample to estimate row size
            sample_query = f"COPY (SELECT * FROM {table_name} LIMIT 1000) TO '{self.temp_dir}/{table_name}_sample.parquet' (FORMAT PARQUET)"
            self.conn.execute(sample_query)

            # Get sample file size to estimate average row size
            sample_file_size = os.path.getsize(
                f"{self.temp_dir}/{table_name}_sample.parquet")
            avg_row_size_mb = (sample_file_size / 1000) / (1024 * 1024)

            # Calculate rows per row group
            rows_per_row_group = int(
                self.target_row_group_size_mb / avg_row_size_mb)

            # Write full table with optimized row groups
            full_query = f"COPY {table_name} TO '{self.target_mount_folder_path}/{table_name}.parquet' (FORMAT PARQUET, ROW_GROUP_SIZE {rows_per_row_group})"
            self.conn.execute(full_query)

        # Clean up
        self.conn.close()
        shutil.rmtree(self.temp_dir)

    def _generate_tables(self):
        '''
        Subclasses should implement this method to return a dictionary of table names and their generation queries.
        '''
        raise NotImplementedError("Subclasses must implement this method.")

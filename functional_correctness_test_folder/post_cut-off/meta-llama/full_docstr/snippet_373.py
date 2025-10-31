
import duckdb
import os
import math


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
        if target_mount_folder_path is not None:
            os.makedirs(target_mount_folder_path, exist_ok=True)

    def _estimate_row_size_mb(self, con, table_name):
        # Create a sample Parquet file to estimate row size
        sample_parquet_file = f'{table_name}_sample.parquet'
        con.sql(
            f"COPY (SELECT * FROM {table_name} USING SAMPLE {10000} ROWS) TO '{sample_parquet_file}' (FORMAT PARQUET)")
        sample_size_bytes = os.path.getsize(sample_parquet_file)
        os.remove(sample_parquet_file)
        # Estimate average row size in MB
        avg_row_size_mb = (sample_size_bytes / (1024 * 1024)) / 10000
        return avg_row_size_mb

    def _write_parquet(self, con, table_name):
        avg_row_size_mb = self._estimate_row_size_mb(con, table_name)
        row_group_size_rows = math.ceil(
            self.target_row_group_size_mb / avg_row_size_mb)
        target_parquet_file = os.path.join(
            self.target_mount_folder_path, f'{table_name}.parquet')
        con.sql(
            f"COPY {table_name} TO '{target_parquet_file}' (FORMAT PARQUET, ROW_GROUP_SIZE {row_group_size_rows})")

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
        con = duckdb.connect(database=':memory:')
        self._generate_data(con)
        for table_name in self._get_table_names():
            self._write_parquet(con, table_name)
        con.close()

    def _generate_data(self, con):
        raise NotImplementedError("Subclasses must implement _generate_data")

    def _get_table_names(self):
        raise NotImplementedError("Subclasses must implement _get_table_names")

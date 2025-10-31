
import duckdb
import os
import math
from typing import List


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
        self.con = duckdb.connect(database=':memory:')

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
        self._generate_data()
        table_names = self._get_table_names()
        for table_name in table_names:
            row_count = self.con.execute(
                f'SELECT COUNT(*) FROM {table_name}').fetchone()[0]
            row_group_size = self._estimate_row_group_size(
                table_name, row_count)
            self._write_to_parquet(table_name, row_count, row_group_size)

    def _generate_data(self):
        # To be implemented by subclasses
        raise NotImplementedError

    def _get_table_names(self) -> List[str]:
        # To be implemented by subclasses
        raise NotImplementedError

    def _estimate_row_group_size(self, table_name: str, row_count: int) -> int:
        sample_size = 1000
        self.con.execute(
            f'COPY (SELECT * FROM {table_name} LIMIT {sample_size}) TO \'sample.parquet\' (FORMAT PARQUET)')
        sample_size_mb = os.path.getsize('sample.parquet') / (1024 * 1024)
        os.remove('sample.parquet')
        avg_row_size_mb = sample_size_mb / sample_size
        row_group_size = math.ceil(
            self.target_row_group_size_mb / avg_row_size_mb)
        return row_group_size

    def _write_to_parquet(self, table_name: str, row_count: int, row_group_size: int):
        if not os.path.exists(self.target_mount_folder_path):
            os.makedirs(self.target_mount_folder_path)
        file_path = os.path.join(
            self.target_mount_folder_path, f'{table_name}.parquet')
        self.con.execute(
            f'COPY {table_name} TO \'{file_path}\' (FORMAT PARQUET, ROW_GROUP_SIZE {row_group_size})')


import duckdb
import os
import math
import pandas as pd
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

    def _estimate_row_size_mb(self, table_name: str, sample_size: int = 10000) -> float:
        '''
        Estimate the average row size in MB by sampling the table.
        '''
        query = f"SELECT * FROM {table_name} LIMIT {sample_size}"
        sample_df = self.con.execute(query).fetchdf()
        sample_size_bytes = sample_df.memory_usage(deep=True).sum()
        return sample_size_bytes / sample_size / (1024 * 1024)

    def _write_parquet_with_row_group_size(self, table_name: str, file_path: str, row_group_size: int):
        '''
        Write the table to a Parquet file with the specified row group size.
        '''
        query = f"COPY {table_name} TO '{file_path}' (FORMAT 'parquet', ROW_GROUP_SIZE {row_group_size})"
        self.con.execute(query)

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
        # Generate tables using the scale factor
        self._generate_tables()

        # Get the list of tables
        tables = self._get_tables()

        for table_name in tables:
            # Estimate the average row size
            row_size_mb = self._estimate_row_size_mb(table_name)

            # Calculate the row group size in rows
            row_group_size_rows = math.ceil(
                self.target_row_group_size_mb / row_size_mb)

            # Write the table to a Parquet file with the calculated row group size
            file_path = os.path.join(
                self.target_mount_folder_path, f'{table_name}.parquet')
            self._write_parquet_with_row_group_size(
                table_name, file_path, row_group_size_rows)

        # Clean up
        self.con.close()

    def _generate_tables(self):
        # This method should be implemented by subclasses to generate the TPC tables
        raise NotImplementedError("Subclasses must implement _generate_tables")

    def _get_tables(self) -> List[str]:
        # This method should be implemented by subclasses to return the list of generated tables
        raise NotImplementedError("Subclasses must implement _get_tables")

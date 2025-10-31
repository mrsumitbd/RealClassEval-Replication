
import duckdb
import os
import shutil
import pandas as pd
from typing import Dict, List


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
        self.con = duckdb.connect("~/tpc_data.db")
        self.tables = {}

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

        if not os.path.exists(self.target_mount_folder_path):
            os.makedirs(self.target_mount_folder_path)

        self._generate_tables()
        self._estimate_row_sizes()
        self._write_parquet_files()

        self.con.close()
        shutil.rmtree("~/tpc_data.db")

    def _generate_tables(self):
        # This method should be overridden by subclasses to generate specific TPC tables
        raise NotImplementedError(
            "This method should be overridden by subclasses.")

    def _estimate_row_sizes(self):
        for table_name, table_df in self.tables.items():
            sample_df = table_df.sample(n=min(1000, len(table_df)))
            sample_parquet_path = os.path.join(
                self.target_mount_folder_path, f"{table_name}_sample.parquet")
            sample_df.to_parquet(sample_parquet_path, row_group_size=1000)
            sample_parquet_size = os.path.getsize(sample_parquet_path)
            average_row_size = sample_parquet_size / len(sample_df)
            os.remove(sample_parquet_path)
            self.tables[table_name]['average_row_size'] = average_row_size

    def _write_parquet_files(self):
        for table_name, table_info in self.tables.items():
            table_df = table_info['data']
            average_row_size = table_info['average_row_size']
            row_group_size = int(
                self.target_row_group_size_mb * 1024 * 1024 / average_row_size)
            parquet_path = os.path.join(
                self.target_mount_folder_path, f"{table_name}.parquet")
            table_df.to_parquet(parquet_path, row_group_size=row_group_size)


import duckdb
import os
import shutil
import pandas as pd


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
        if not self.target_mount_folder_path:
            raise ValueError("Target mount folder path must be specified.")

        if not os.path.exists(self.target_mount_folder_path):
            os.makedirs(self.target_mount_folder_path)

        self._generate_tables()
        for table in self.tables:
            self._write_table_to_parquet(table)

        self.con.close()
        shutil.rmtree("~/tpc_data.db")

    def _generate_tables(self):
        # This method should be overridden by subclasses to generate specific TPC tables
        raise NotImplementedError(
            "This method should be overridden by subclasses.")

    def _write_table_to_parquet(self, table_name: str):
        # Create a sample to estimate row size
        sample_df = self.con.execute(
            f"SELECT * FROM {table_name} LIMIT 1000").fetchdf()
        sample_size_mb = sample_df.memory_usage(deep=True).sum() / (1024 ** 2)
        avg_row_size_mb = sample_size_mb / \
            len(sample_df) if len(sample_df) > 0 else 0

        if avg_row_size_mb == 0:
            raise ValueError("Average row size could not be determined.")

        rows_per_row_group = int(
            self.target_row_group_size_mb / avg_row_size_mb)
        if rows_per_row_group <= 0:
            rows_per_row_group = 1

        # Write the full table to Parquet with the calculated row group size
        self.con.execute(f"COPY (SELECT * FROM {table_name}) TO '{os.path.join(self.target_mount_folder_path, table_name)}.parquet' (FORMAT PARQUET, ROW_GROUP_SIZE {rows_per_row_group})"

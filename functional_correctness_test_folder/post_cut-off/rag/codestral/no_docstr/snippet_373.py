
import duckdb
import os
import shutil
import tempfile
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
        self.temp_dir = tempfile.mkdtemp()

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
        try:
            # Generate the schema and data for the specific TPC benchmark
            self._generate_schema()
            self._generate_data()

            # Get the list of tables to process
            tables = self._get_tables()

            # Process each table
            for table in tables:
                # Create a sample Parquet file to estimate row size
                sample_file = os.path.join(
                    self.temp_dir, f"{table}_sample.parquet")
                self._write_sample_parquet(table, sample_file)

                # Estimate the average row size in MB
                avg_row_size_mb = self._estimate_row_size(sample_file)

                # Calculate the number of rows per row group
                rows_per_row_group = int(
                    self.target_row_group_size_mb / avg_row_size_mb)

                # Write the full table to Parquet with optimized row group size
                output_file = os.path.join(
                    self.target_mount_folder_path, f"{table}.parquet")
                self._write_full_parquet(
                    table, output_file, rows_per_row_group)

        finally:
            # Clean up temporary files and in-memory tables
            self._cleanup()

    def _generate_schema(self):
        '''
        Generate the schema for the TPC benchmark.
        This method should be implemented by subclasses.
        '''
        raise NotImplementedError

    def _generate_data(self):
        '''
        Generate the data for the TPC benchmark.
        This method should be implemented by subclasses.
        '''
        raise NotImplementedError

    def _get_tables(self) -> List[str]:
        '''
        Get the list of tables to process.
        This method should be implemented by subclasses.
        '''
        raise NotImplementedError

    def _write_sample_parquet(self, table: str, output_file: str):
        '''
        Write a sample of the table to a Parquet file.
        :param table: The name of the table to sample.
        :param output_file: The path to the output Parquet file.
        '''
        query = f"SELECT * FROM {table} LIMIT 10000"
        self.conn.execute(
            f"COPY ({query}) TO '{output_file}' (FORMAT PARQUET)")

    def _estimate_row_size(self, parquet_file: str) -> float:
        '''
        Estimate the average row size in MB from a Parquet file.
        :param parquet_file: The path to the Parquet file.
        :return: The average row size in MB.
        '''
        file_size_mb = os.path.getsize(parquet_file) / (1024 * 1024)
        row_count = self.conn.execute(
            f"SELECT COUNT(*) FROM parquet_scan('{parquet_file}')").fetchone()[0]
        return file_size_mb / row_count

    def _write_full_parquet(self, table: str, output_file: str, rows_per_row_group: int):
        '''
        Write the full table to a Parquet file with optimized row group size.
        :param table: The name of the table to write.
        :param output_file: The path to the output Parquet file.
        :param rows_per_row_group: The number of rows per row group.
        '''
        query = f"SELECT * FROM {table}"
        self.conn.execute(
            f"COPY ({query}) TO '{output_file}' (FORMAT PARQUET, ROW_GROUP_SIZE {rows_per_row_group})")

    def _cleanup(self):
        '''
        Clean up temporary files and in-memory tables.
        '''
        shutil.rmtree(self.temp_dir)
        self.conn.close()

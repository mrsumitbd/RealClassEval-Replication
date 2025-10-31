
import os
import duckdb
import shutil
import tempfile
import math


class _TPCDataGenerator:
    '''
    Base class for TPC data generation. PLEASE DO NOT INSTANTIATE THIS CLASS DIRECTLY. Use the TPCHDataGenerator and TPCDSDataGenerator
    subclasses instead.
    '''

    def __init__(self, scale_factor: int, target_mount_folder_path: str = None, target_row_group_size_mb: int = 128):
        self.scale_factor = scale_factor
        self.target_mount_folder_path = target_mount_folder_path
        self.target_row_group_size_mb = target_row_group_size_mb
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
        conn = duckdb.connect()
        try:
            self._generate_tables(conn)
            self._write_parquet_files(conn)
        finally:
            conn.close()
            shutil.rmtree(self.temp_dir)

    def _generate_tables(self, conn):
        raise NotImplementedError("Subclasses must implement this method.")

    def _write_parquet_files(self, conn):
        for table_name in self._get_table_names():
            sample_file = os.path.join(
                self.temp_dir, f"{table_name}_sample.parquet")
            conn.execute(
                f"COPY (SELECT * FROM {table_name} LIMIT 1000) TO '{sample_file}' (FORMAT PARQUET);")
            row_size_mb = self._estimate_row_size_mb(sample_file)
            rows_per_row_group = math.ceil(
                self.target_row_group_size_mb / row_size_mb)
            target_file = os.path.join(
                self.target_mount_folder_path, f"{table_name}.parquet")
            conn.execute(
                f"COPY (SELECT * FROM {table_name}) TO '{target_file}' (FORMAT PARQUET, ROW_GROUP_SIZE {rows_per_row_group});")

    def _estimate_row_size_mb(self, file_path):
        file_size_bytes = os.path.getsize(file_path)
        file_size_mb = file_size_bytes / (1024 * 1024)
        num_rows = duckdb.execute(
            f"SELECT COUNT(*) FROM '{file_path}'").fetchone()[0]
        return file_size_mb / num_rows

    def _get_table_names(self):
        raise NotImplementedError("Subclasses must implement this method.")


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

    def __init__(self, scale_factor: int, target_mount_folder_path: Optional[str] = None, target_row_group_size_mb: int = 128):
        self.scale_factor = scale_factor
        self.target_mount_folder_path = target_mount_folder_path
        self.target_row_group_size_mb = target_row_group_size_mb
        self._temp_dir = tempfile.mkdtemp()
        self._conn = duckdb.connect()

    def _generate_tables(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def _estimate_row_size(self, table_name: str) -> float:
        sample_path = os.path.join(
            self._temp_dir, f"{table_name}_sample.parquet")
        self._conn.execute(
            f"COPY (SELECT * FROM {table_name} LIMIT 1000) TO '{sample_path}' (FORMAT PARQUET)")
        file_size = os.path.getsize(sample_path)
        avg_row_size = file_size / 1000 / (1024 * 1024)  # MB per row
        os.remove(sample_path)
        return avg_row_size

    def _write_optimized_parquet(self, table_name: str):
        avg_row_size = self._estimate_row_size(table_name)
        rows_per_group = int(self.target_row_group_size_mb / avg_row_size)

        if self.target_mount_folder_path:
            output_path = os.path.join(
                self.target_mount_folder_path, f"{table_name}.parquet")
            self._conn.execute(
                f"COPY {table_name} TO '{output_path}' (FORMAT PARQUET, ROW_GROUP_SIZE {rows_per_group})"
            )

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
            self._generate_tables()
            tables = self._conn.execute("SHOW TABLES").fetchall()
            for table in tables:
                table_name = table[0]
                self._write_optimized_parquet(table_name)
        finally:
            self._conn.close()
            shutil.rmtree(self._temp_dir, ignore_errors=True)

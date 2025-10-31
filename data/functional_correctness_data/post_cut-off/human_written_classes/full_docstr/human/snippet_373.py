import os
import posixpath
import importlib.util

class _TPCDataGenerator:
    """
    Base class for TPC data generation. PLEASE DO NOT INSTANTIATE THIS CLASS DIRECTLY. Use the TPCHDataGenerator and TPCDSDataGenerator
    subclasses instead.
    """
    GEN_UTIL = ''

    def __init__(self, scale_factor: int, target_mount_folder_path: str=None, target_row_group_size_mb: int=128):
        """
        Initialize the TPC data generator with a scale factor.

        :param scale_factor: The scale factor for the data generation.
        """
        self.scale_factor = scale_factor
        self.target_mount_folder_path = target_mount_folder_path
        self.target_row_group_size_mb = target_row_group_size_mb
        if importlib.util.find_spec('duckdb') is None:
            raise ImportError('DuckDB is used for data generation but is not installed. Install using `%pip install lakebench[duckdb]` or `%pip install lakebench[datagen]`')

    def run(self):
        """
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
        """
        import duckdb
        import pyarrow.parquet as pq
        con = duckdb.connect()
        print(f'Generating in-memory tables')
        con.execute(f'CALL {self.GEN_UTIL}(sf={self.scale_factor})')
        tables = [row[0] for row in con.execute('SHOW TABLES').fetchall()]
        print(f'Generated in-memory tables: {tables}')
        for table in tables:
            sample_file = posixpath.join(self.target_mount_folder_path, f'{table}_sample.parquet')
            full_folder_path = posixpath.join(self.target_mount_folder_path, table)
            os.makedirs(self.target_mount_folder_path, exist_ok=True)
            print(f'\nSampling {table} to evaluate row count to target {self.target_row_group_size_mb}mb row groups...')
            con.execute(f"\n                COPY (SELECT * FROM {table} LIMIT 1000000)\n                TO '{sample_file}'\n                (FORMAT 'parquet')\n            ")
            pf = pq.ParquetFile(sample_file)
            rg = pf.metadata.row_group(0)
            avg_row_size = rg.total_byte_size / rg.num_rows
            target_size_bytes = self.target_row_group_size_mb * 1024 * 1024
            target_rows = int(target_size_bytes / avg_row_size)
            print(f'Writing {table} to {full_folder_path} with ROW_GROUP_SIZE {target_rows}...')
            con.execute(f"\n                COPY {table} TO '{full_folder_path}'\n                (FORMAT 'parquet', ROW_GROUP_SIZE {target_rows}, PER_THREAD_OUTPUT)\n            ")
            con.execute(f'DROP TABLE {table}')
            os.remove(sample_file)
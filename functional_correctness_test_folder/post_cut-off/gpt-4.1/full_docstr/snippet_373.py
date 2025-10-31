
import os
import tempfile
import shutil
import duckdb


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
        self.target_mount_folder_path = target_mount_folder_path or os.getcwd()
        self.target_row_group_size_mb = target_row_group_size_mb
        self._duckdb_conn = duckdb.connect(database=':memory:')
        self._table_names = self._get_table_names()

    def _get_table_names(self):
        '''
        Should be implemented by subclasses to return the list of TPC table names.
        '''
        raise NotImplementedError(
            "Subclasses must implement _get_table_names()")

    def _create_tables(self):
        '''
        Should be implemented by subclasses to create TPC tables in DuckDB.
        '''
        raise NotImplementedError("Subclasses must implement _create_tables()")

    def run(self):
        '''
        This method uses DuckDB to generate in-memory tables based on the specified 
        scale factor and writes them to Parquet files. It estimates the average row 
        size in MB using a sample of the data since DuckDB only supports specifying 
        the number of rows per row group. The generated tables are written to the 
        specified target folder with optimized row group sizes.
        '''
        self._create_tables()
        os.makedirs(self.target_mount_folder_path, exist_ok=True)
        for table in self._table_names:
            # Estimate row size using a sample
            sample_rows = 10000
            tmp_dir = tempfile.mkdtemp()
            sample_file = os.path.join(tmp_dir, f"{table}_sample.parquet")
            # Write sample
            self._duckdb_conn.execute(
                f"COPY (SELECT * FROM {table} LIMIT {sample_rows}) TO '{sample_file}' (FORMAT 'parquet')"
            )
            # Get file size
            sample_file_size = os.path.getsize(sample_file)
            # Estimate row size in bytes
            avg_row_size_bytes = sample_file_size / sample_rows
            avg_row_size_mb = avg_row_size_bytes / (1024 * 1024)
            # Get total row count
            total_rows = self._duckdb_conn.execute(
                f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            # Calculate rows per row group
            if avg_row_size_mb > 0:
                rows_per_row_group = int(
                    self.target_row_group_size_mb / avg_row_size_mb)
            else:
                rows_per_row_group = 1000000  # fallback
            # at least 1000 rows per group
            rows_per_row_group = max(1000, rows_per_row_group)
            # Write full table to Parquet
            target_file = os.path.join(
                self.target_mount_folder_path, f"{table}.parquet")
            self._duckdb_conn.execute(
                f"COPY {table} TO '{target_file}' (FORMAT 'parquet', ROW_GROUP_SIZE={rows_per_row_group})"
            )
            # Clean up
            shutil.rmtree(tmp_dir)
            self._duckdb_conn.execute(f"DROP TABLE IF EXISTS {table}")

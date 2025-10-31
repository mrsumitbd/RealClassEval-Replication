
import os
import shutil
import tempfile
import duckdb


class _TPCDataGenerator:
    '''
    Base class for TPC data generation. PLEASE DO NOT INSTANTIATE THIS CLASS DIRECTLY. Use the TPCHDataGenerator and TPCDSDataGenerator
    subclasses instead.
    '''

    def __init__(self, scale_factor: int, target_mount_folder_path: str = None, target_row_group_size_mb: int = 128):
        if type(self) is _TPCDataGenerator:
            raise TypeError(
                "Do not instantiate _TPCDataGenerator directly. Use a subclass.")
        self.scale_factor = scale_factor
        self.target_mount_folder_path = target_mount_folder_path or os.path.abspath(
            "tpc_data")
        self.target_row_group_size_mb = target_row_group_size_mb
        self._duckdb_conn = None
        self._table_names = []  # Subclasses should set this
        # Subclasses should set this: {table_name: SQL or function}
        self._table_generators = {}

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
        os.makedirs(self.target_mount_folder_path, exist_ok=True)
        self._duckdb_conn = duckdb.connect(database=':memory:')
        conn = self._duckdb_conn

        for table in self._table_names:
            # 1. Generate table in DuckDB
            generator = self._table_generators[table]
            if callable(generator):
                generator(conn, self.scale_factor)
            else:
                conn.execute(generator.format(scale_factor=self.scale_factor))

            # 2. Estimate row size using a sample
            sample_file = tempfile.NamedTemporaryFile(
                delete=False, suffix=".parquet")
            sample_file.close()
            sample_rows = 10000
            conn.execute(
                f"COPY (SELECT * FROM {table} LIMIT {sample_rows}) TO '{sample_file.name}' (FORMAT 'parquet')")
            sample_size_bytes = os.path.getsize(sample_file.name)
            avg_row_size_bytes = sample_size_bytes / sample_rows if sample_rows else 1
            os.unlink(sample_file.name)

            # 3. Get total row count
            total_rows = conn.execute(
                f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            if total_rows == 0:
                continue

            # 4. Calculate rows per row group
            target_bytes = self.target_row_group_size_mb * 1024 * 1024
            rows_per_group = max(1, int(target_bytes // avg_row_size_bytes))

            # 5. Write full table to Parquet with optimized row group size
            target_file = os.path.join(
                self.target_mount_folder_path, f"{table}.parquet")
            conn.execute(
                f"COPY {table} TO '{target_file}' (FORMAT 'parquet', ROW_GROUP_SIZE={rows_per_group})"
            )

            # 6. Clean up in-memory table
            conn.execute(f"DROP TABLE IF EXISTS {table}")

        conn.close()
        self._duckdb_conn = None

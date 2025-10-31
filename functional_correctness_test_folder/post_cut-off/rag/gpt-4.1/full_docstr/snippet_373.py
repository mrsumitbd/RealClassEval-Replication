import os
import duckdb
import tempfile
import shutil


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
        self.duckdb_conn = duckdb.connect(database=':memory:')
        self.table_names = []
        self.tpc_type = None  # Should be set by subclass, e.g., 'tpch' or 'tpcds'

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
        if not self.tpc_type or not self.table_names:
            raise NotImplementedError(
                "Subclasses must set self.tpc_type and self.table_names.")

        os.makedirs(self.target_mount_folder_path, exist_ok=True)
        conn = self.duckdb_conn

        for table in self.table_names:
            # 1. Generate the table in DuckDB
            table_sql = f"CALL {self.tpc_type}.sf{self.scale_factor}('{table}');"
            try:
                conn.execute(table_sql)
            except Exception as e:
                raise RuntimeError(f"Failed to generate table {table}: {e}")

            # 2. Estimate average row size using a sample
            sample_file = tempfile.NamedTemporaryFile(
                delete=False, suffix='.parquet')
            sample_file_path = sample_file.name
            sample_file.close()
            try:
                # Write a sample of 10000 rows to Parquet
                conn.execute(
                    f"COPY (SELECT * FROM {table} LIMIT 10000) TO '{sample_file_path}' (FORMAT PARQUET);")
                sample_size_bytes = os.path.getsize(sample_file_path)
                # Get actual number of rows in sample (could be < 10000 for small tables)
                sample_row_count = conn.execute(
                    f"SELECT COUNT(*) FROM {table} LIMIT 10000").fetchone()[0]
                avg_row_size_bytes = sample_size_bytes / \
                    sample_row_count if sample_row_count else 1
            finally:
                os.remove(sample_file_path)

            # 3. Get total row count for the table
            total_rows = conn.execute(
                f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            if total_rows == 0:
                continue

            # 4. Calculate optimal row group size in rows
            target_row_group_size_bytes = self.target_row_group_size_mb * 1024 * 1024
            rows_per_group = max(
                1, int(target_row_group_size_bytes / avg_row_size_bytes))

            # 5. Write the full table to Parquet with optimized row group size
            target_file = os.path.join(
                self.target_mount_folder_path, f"{table}.parquet")
            conn.execute(
                f"COPY {table} TO '{target_file}' (FORMAT PARQUET, ROW_GROUP_SIZE={rows_per_group});"
            )

            # 6. Drop the in-memory table to free up memory
            conn.execute(f"DROP TABLE IF EXISTS {table};")

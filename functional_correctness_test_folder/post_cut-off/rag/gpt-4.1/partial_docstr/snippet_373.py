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
        self.tpc_schema = None  # To be set by subclass

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
        if not self.table_names or not self.tpc_schema:
            raise NotImplementedError(
                "Subclasses must set self.table_names and self.tpc_schema.")

        os.makedirs(self.target_mount_folder_path, exist_ok=True)
        conn = self.duckdb_conn

        for table in self.table_names:
            # 1. Create the TPC table in DuckDB
            create_sql = f"CREATE TABLE {table} AS SELECT * FROM {self.tpc_schema}('{table}', {self.scale_factor});"
            conn.execute(f"DROP TABLE IF EXISTS {table};")
            conn.execute(create_sql)

            # 2. Estimate row size using a sample
            sample_rows = 10000
            tmp_dir = tempfile.mkdtemp()
            sample_file = os.path.join(tmp_dir, f"{table}_sample.parquet")
            conn.execute(
                f"COPY (SELECT * FROM {table} LIMIT {sample_rows}) TO '{sample_file}' (FORMAT 'parquet');")
            sample_size_bytes = os.path.getsize(sample_file)
            avg_row_size_bytes = sample_size_bytes / sample_rows if sample_rows else 1
            shutil.rmtree(tmp_dir)

            # 3. Get total row count
            row_count = conn.execute(
                f"SELECT COUNT(*) FROM {table};").fetchone()[0]
            if row_count == 0:
                continue

            # 4. Calculate rows per row group
            target_row_group_size_bytes = self.target_row_group_size_mb * 1024 * 1024
            rows_per_row_group = max(
                1, int(target_row_group_size_bytes // avg_row_size_bytes))

            # 5. Write full table to Parquet with optimized row group size
            out_file = os.path.join(
                self.target_mount_folder_path, f"{table}.parquet")
            conn.execute(
                f"COPY {table} TO '{out_file}' (FORMAT 'parquet', ROW_GROUP_SIZE={rows_per_row_group});"
            )

            # 6. Drop the table from memory
            conn.execute(f"DROP TABLE IF EXISTS {table};")


class _TPCDataGenerator:
    '''
    Base class for TPC data generation. PLEASE DO NOT INSTANTIATE THIS CLASS DIRECTLY. Use the TPCHDataGenerator and TPCDSDataGenerator
    subclasses instead.
    '''

    def __init__(self, scale_factor: int, target_mount_folder_path: str = None, target_row_group_size_mb: int = 128):
        '''
        Initialize the TPC data generator with a scale factor.
        :param scale_factor: The scale factor for the data generation.
        :param target_mount_folder_path: The target folder path where Parquet files will be written.
        :param target_row_group_size_mb: The target row group size in MB (default: 128).
        '''
        self.scale_factor = scale_factor
        self.target_mount_folder_path = target_mount_folder_path
        self.target_row_group_size_mb = target_row_group_size_mb

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
        import duckdb
        import os
        import tempfile
        import shutil

        if not self.target_mount_folder_path:
            raise ValueError("Target mount folder path must be specified.")

        os.makedirs(self.target_mount_folder_path, exist_ok=True)
        temp_dir = tempfile.mkdtemp()

        try:
            conn = duckdb.connect(database=':memory:')
            tables = self._get_table_names()

            for table in tables:
                # Generate sample data to estimate row size
                sample_query = f"SELECT * FROM {self._get_table_query(table)} USING SAMPLE 1000"
                sample_file = os.path.join(temp_dir, f"{table}_sample.parquet")
                conn.execute(
                    f"COPY ({sample_query}) TO '{sample_file}' (FORMAT PARQUET)")

                # Estimate row size
                sample_size_mb = os.path.getsize(sample_file) / (1024 * 1024)
                avg_row_size_mb = sample_size_mb / 1000
                rows_per_group = int(
                    self.target_row_group_size_mb / avg_row_size_mb)

                # Generate full table with optimized row group size
                full_query = f"SELECT * FROM {self._get_table_query(table)}"
                output_file = os.path.join(
                    self.target_mount_folder_path, f"{table}.parquet")
                conn.execute(
                    f"COPY ({full_query}) TO '{output_file}' (FORMAT PARQUET, ROW_GROUP_SIZE {rows_per_group})")

        finally:
            conn.close()
            shutil.rmtree(temp_dir)

    def _get_table_names(self):
        '''
        Returns a list of table names to generate. Must be implemented by subclasses.
        '''
        raise NotImplementedError("Subclasses must implement this method.")

    def _get_table_query(self, table_name):
        '''
        Returns the SQL query to generate the specified table. Must be implemented by subclasses.
        '''
        raise NotImplementedError("Subclasses must implement this method.")

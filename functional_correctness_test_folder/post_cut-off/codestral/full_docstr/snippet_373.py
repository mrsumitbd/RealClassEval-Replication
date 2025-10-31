
import duckdb
import os
import shutil
import tempfile


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
        temp_dir = tempfile.mkdtemp()
        try:
            for table in self.tables:
                # Create sample table
                sample_table = f"{table}_sample"
                self.conn.execute(
                    f"CREATE TABLE {sample_table} AS SELECT * FROM {table} LIMIT 10000")

                # Write sample table to Parquet
                sample_parquet_path = os.path.join(
                    temp_dir, f"{sample_table}.parquet")
                self.conn.execute(
                    f"COPY {sample_table} TO '{sample_parquet_path}' (FORMAT PARQUET)")

                # Estimate row size
                sample_size_mb = os.path.getsize(
                    sample_parquet_path) / (1024 * 1024)
                row_size_mb = sample_size_mb / 10000

                # Calculate row group size
                row_group_size = int(
                    self.target_row_group_size_mb / row_size_mb)

                # Write full table to Parquet with optimized row group size
                parquet_path = os.path.join(
                    self.target_mount_folder_path, f"{table}.parquet")
                self.conn.execute(
                    f"COPY {table} TO '{parquet_path}' (FORMAT PARQUET, ROW_GROUP_SIZE {row_group_size})")

                # Clean up sample table
                self.conn.execute(f"DROP TABLE {sample_table}")
                os.remove(sample_parquet_path)

        finally:
            # Clean up temporary directory
            shutil.rmtree(temp_dir)
            self.conn.close()

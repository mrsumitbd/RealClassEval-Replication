
import duckdb
import os
import pandas as pd


class _TPCDataGenerator:
    '''
    Base class for TPC data generation. PLEASE DO NOT INSTANTIATE THIS CLASS DIRECTLY. Use the TPCHDataGenerator and TPCDSDataGenerator
    subclasses instead.
    '''

    def __init__(self, scale_factor: int, target_mount_folder_path: str = None, target_row_group_size_mb: int = 128):
        self.scale_factor = scale_factor
        self.target_mount_folder_path = target_mount_folder_path
        self.target_row_group_size_mb = target_row_group_size_mb
        self.con = duckdb.connect(database=':memory:')

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
        # Create target directory if it doesn't exist
        if self.target_mount_folder_path is not None:
            os.makedirs(self.target_mount_folder_path, exist_ok=True)

        # Generate TPC data using DuckDB
        self._generate_data()

        # Get the list of tables
        tables = self.con.execute("SHOW TABLES").fetchall()
        tables = [table[0] for table in tables]

        for table in tables:
            # Estimate the average row size in MB
            sample_file_path = os.path.join(
                self.target_mount_folder_path, f'{table}_sample.parquet') if self.target_mount_folder_path else f'{table}_sample.parquet'
            self.con.execute(
                f"COPY (SELECT * FROM {table} LIMIT 10000) TO '{sample_file_path}' (FORMAT PARQUET)")
            sample_df = pd.read_parquet(sample_file_path)
            avg_row_size_mb = sample_df.memory_usage(
                deep=True).sum() / (1024 * 1024 * len(sample_df))
            os.remove(sample_file_path)

            # Calculate the optimal row group size
            row_group_size_rows = int(
                self.target_row_group_size_mb / avg_row_size_mb)

            # Write the full table to Parquet files with optimized row group sizes
            target_file_path = os.path.join(
                self.target_mount_folder_path, f'{table}.parquet') if self.target_mount_folder_path else f'{table}.parquet'
            self.con.execute(
                f"COPY {table} TO '{target_file_path}' (FORMAT PARQUET, ROW_GROUP_SIZE {row_group_size_rows})")

        # Clean up
        self.con.close()

    def _generate_data(self):
        # This method should be implemented by the subclasses
        raise NotImplementedError(
            "Subclasses must implement the _generate_data method")


class _TPCDataGenerator:
    '''
    Base class for TPC data generation. PLEASE DO NOT INSTANTIATE THIS CLASS DIRECTLY. Use the TPCHDataGenerator and TPCDSDataGenerator
    subclasses instead.
        '''

    def __init__(self, scale_factor: int, target_mount_folder_path: str = None, target_row_group_size_mb: int = 128):
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
        import pandas as pd

        # Connect to an in-memory DuckDB database
        con = duckdb.connect("~/tpc_data.duckdb")

        # Generate sample data to estimate row size
        self._generate_sample_data(con)
        row_size_mb = self._estimate_row_size(con)

        # Calculate the number of rows per row group
        rows_per_row_group = int(
            (self.target_row_group_size_mb * 1024 * 1024) / row_size_mb)

        # Generate full data and write to Parquet
        self._generate_full_data(con)
        self._write_to_parquet(con, rows_per_row_group)

        # Clean up
        con.execute("DROP TABLE IF EXISTS sample_table")
        con.execute("DROP TABLE IF EXISTS full_table")
        con.close()
        os.remove("~/tpc_data.duckdb")

    def _generate_sample_data(self, con):
        # Placeholder for sample data generation logic
        con.execute(
            f"CREATE TABLE sample_table AS SELECT * FROM generate_series(1, 1000) AS id")

    def _estimate_row_size(self, con):
        # Placeholder for row size estimation logic
        sample_df = con.execute("SELECT * FROM sample_table").fetchdf()
        row_size_mb = sample_df.memory_usage(
            deep=True).sum() / (1024 * 1024) / len(sample_df)
        return row_size_mb

    def _generate_full_data(self, con):
        # Placeholder for full data generation logic
        con.execute(
            f"CREATE TABLE full_table AS SELECT * FROM generate_series(1, {self.scale_factor * 1000}) AS id")

    def _write_to_parquet(self, con, rows_per_row_group):
        # Placeholder for writing to Parquet logic
        con.execute(f"COPY full_table TO '{self.target_mount_folder_path}/full_table.parquet' (FORMAT PARQUET, ROW_GROUP_SIZE {rows_per_row_group})"

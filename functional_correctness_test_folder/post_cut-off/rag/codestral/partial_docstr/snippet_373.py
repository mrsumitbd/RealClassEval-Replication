
import duckdb
import os
import shutil
import tempfile
from typing import Dict, List, Optional


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
        self.temp_dir = tempfile.mkdtemp()
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
        try:
            # Generate the schema and tables
            self._generate_schema()
            self._generate_tables()

            # Get the list of tables to process
            tables = self._get_tables()

            # Process each table
            for table in tables:
                self._process_table(table)

        finally:
            # Clean up
            self.conn.close()
            shutil.rmtree(self.temp_dir)

    def _generate_schema(self):
        '''
        Generate the schema for the TPC data.
        '''
        raise NotImplementedError("Subclasses must implement this method.")

    def _generate_tables(self):
        '''
        Generate the tables for the TPC data.
        '''
        raise NotImplementedError("Subclasses must implement this method.")

    def _get_tables(self) -> List[str]:
        '''
        Get the list of tables to process.
        '''
        raise NotImplementedError("Subclasses must implement this method.")

    def _process_table(self, table: str):
        '''
        Process a single table: estimate row size, write to Parquet, and clean up.
        '''
        # Create a sample Parquet file to estimate row size
        sample_file = os.path.join(self.temp_dir, f"{table}_sample.parquet")
        self.conn.execute(
            f"COPY (SELECT * FROM {table} LIMIT 1000) TO '{sample_file}' (FORMAT PARQUET)")

        # Estimate row size
        row_size_mb = self._estimate_row_size(sample_file)

        # Calculate rows per row group
        rows_per_row_group = int(self.target_row_group_size_mb / row_size_mb)

        # Write the full table to Parquet with optimized row group size
        target_file = os.path.join(
            self.target_mount_folder_path, f"{table}.parquet")
        self.conn.execute(f"""
            COPY (SELECT * FROM {table})
            TO '{target_file}'
            (FORMAT PARQUET, ROW_GROUP_SIZE {rows_per_row_group})
        """)

        # Clean up the sample file
        os.remove(sample_file)

    def _estimate_row_size(self, sample_file: str) -> float:
        '''
        Estimate the average row size in MB from a sample Parquet file.
        '''
        # Get the file size in bytes
        file_size_bytes = os.path.getsize(sample_file)

        # Get the number of rows in the sample
        num_rows = self.conn.execute(
            f"SELECT COUNT(*) FROM parquet_scan('{sample_file}')").fetchone()[0]

        # Calculate average row size in MB
        if num_rows == 0:
            return 0.0
        return (file_size_bytes / num_rows) / (1024 * 1024)

import os
import tempfile
import math
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
        if not isinstance(scale_factor, int) or scale_factor <= 0:
            raise ValueError("scale_factor must be a positive integer")
        if not isinstance(target_row_group_size_mb, int) or target_row_group_size_mb <= 0:
            raise ValueError(
                "target_row_group_size_mb must be a positive integer")

        self.scale_factor: int = scale_factor
        self.target_row_group_size_mb: int = target_row_group_size_mb

        # Infer extension and generator proc from subclass name if not provided by subclass
        # Subclasses may predefine: self._extension_name and self._generator_proc
        cls_name = self.__class__.__name__.lower()
        if not hasattr(self, '_extension_name') or getattr(self, '_extension_name') is None:
            if 'tpch' in cls_name:
                self._extension_name = 'tpch'
            elif 'tpcds' in cls_name:
                self._extension_name = 'tpcds'
            else:
                self._extension_name = None
        if not hasattr(self, '_generator_proc') or getattr(self, '_generator_proc') is None:
            if 'tpch' in cls_name:
                self._generator_proc = 'dbgen'
            elif 'tpcds' in cls_name:
                self._generator_proc = 'dsgen'
            else:
                self._generator_proc = None

        if target_mount_folder_path is None:
            root = os.path.join(os.getcwd(), 'tpc_output')
            bench = self._extension_name or 'tpc'
            self.target_mount_folder_path = os.path.join(
                root, bench, f'sf_{self.scale_factor}')
        else:
            self.target_mount_folder_path = target_mount_folder_path

        os.makedirs(self.target_mount_folder_path, exist_ok=True)

        # Will be populated by run()
        self._generated_tables: List[str] = []
        self._output_files: Dict[str, str] = {}

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
        if not self._extension_name or not self._generator_proc:
            raise RuntimeError(
                "This base class cannot run directly. Subclasses must define _extension_name and _generator_proc.")

        try:
            import duckdb  # Imported here to avoid hard dependency if unused
        except Exception as e:
            raise RuntimeError(
                "duckdb is required to generate TPC data") from e

        con = duckdb.connect(database=':memory:')
        try:
            con.execute(f"INSTALL {self._extension_name};")
        except Exception:
            # Extension may already be present in some environments; ignore install errors
            pass
        con.execute(f"LOAD {self._extension_name};")

        # Generate in-memory tables
        # Example: CALL dbgen(sf=1) or CALL dsgen(sf=1)
        con.execute(
            f"CALL {self._generator_proc}(sf={int(self.scale_factor)});")

        # List generated tables
        tables = [r[0] for r in con.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='main' AND table_type='BASE TABLE';"
        ).fetchall()]

        self._generated_tables = tables

        # For each table, estimate bytes/row using a sample parquet, then write full parquet with chosen row_group_size
        for tbl in tables:
            # Total rows
            total_rows = con.execute(
                f"SELECT COUNT(*) FROM {duckdb.escape_identifier(tbl)}").fetchone()[0]
            if total_rows == 0:
                continue

            # Sample to estimate row size
            sample_rows = max(1, min(total_rows, 100_000))
            with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmpf:
                tmp_path = tmpf.name
            try:
                con.execute(
                    f"COPY (SELECT * FROM {duckdb.escape_identifier(tbl)} LIMIT {sample_rows}) "
                    f"TO '{tmp_path}' (FORMAT 'parquet');"
                )
                file_size_bytes = os.path.getsize(tmp_path)
                # Avoid division by zero
                avg_bytes_per_row = max(
                    1, file_size_bytes // sample_rows if sample_rows > 0 else file_size_bytes)
            finally:
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

            # Compute row_group_size (in rows) based on target MB
            target_bytes = self.target_row_group_size_mb * 1024 * 1024
            rows_per_group = max(1, int(target_bytes / avg_bytes_per_row))
            # Clamp to reasonable bounds
            rows_per_group = max(10, min(rows_per_group, 10_000_000))

            # Write full table to parquet
            out_path = os.path.join(
                self.target_mount_folder_path, f"{tbl}.parquet")
            con.execute(
                f"COPY {duckdb.escape_identifier(tbl)} TO '{out_path}' "
                f"(FORMAT 'parquet', ROW_GROUP_SIZE {rows_per_group});"
            )
            self._output_files[tbl] = out_path

        # Cleanup in-memory tables
        for tbl in tables:
            try:
                con.execute(f"DROP TABLE {duckdb.escape_identifier(tbl)};")
            except Exception:
                pass

        con.close()

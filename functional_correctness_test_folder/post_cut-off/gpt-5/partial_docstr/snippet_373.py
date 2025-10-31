import os
import tempfile
import shutil
from typing import List, Optional


class _TPCDataGenerator:
    '''
    Base class for TPC data generation. PLEASE DO NOT INSTANTIATE THIS CLASS DIRECTLY. Use the TPCHDataGenerator and TPCDSDataGenerator
    subclasses instead.
    '''

    def __init__(self, scale_factor: int, target_mount_folder_path: str = None, target_row_group_size_mb: int = 128):
        if not isinstance(scale_factor, int) or scale_factor <= 0:
            raise ValueError("scale_factor must be a positive integer")
        if not isinstance(target_row_group_size_mb, int) or target_row_group_size_mb <= 0:
            raise ValueError(
                "target_row_group_size_mb must be a positive integer")

        self.scale_factor = scale_factor
        self.target_row_group_size_mb = target_row_group_size_mb

        if target_mount_folder_path is None:
            self.target_mount_folder_path = os.path.abspath(os.getcwd())
        else:
            self.target_mount_folder_path = os.path.abspath(
                target_mount_folder_path)

        os.makedirs(self.target_mount_folder_path, exist_ok=True)

        # Subclasses are expected to set these:
        # self._duckdb_extension: str  (e.g., "tpch" or "tpcds")
        # self._duckdb_generator_proc: str  (e.g., "dbgen" or "dsdgen")
        # Optionally, self._schema: str (defaults to 'main')
        # Optionally, self._table_names: List[str] to restrict
        # Example subclass:
        #   self._duckdb_extension = "tpch"
        #   self._duckdb_generator_proc = "dbgen"

    def run(self) -> List[str]:
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
            import duckdb
        except Exception as e:
            raise RuntimeError(
                "duckdb is required to run data generation") from e

        if not hasattr(self, "_duckdb_extension") or not hasattr(self, "_duckdb_generator_proc"):
            raise NotImplementedError(
                "Subclass must define _duckdb_extension and _duckdb_generator_proc attributes")

        schema = getattr(self, "_schema", "main")
        output_files: List[str] = []
        conn = duckdb.connect(database=":memory:")
        tmp_dir = tempfile.mkdtemp(prefix="_tpcgen_")
        try:
            conn.execute(f"INSTALL {self._duckdb_extension}")
            conn.execute(f"LOAD {self._duckdb_extension}")

            # Generate data
            # DuckDB generator procs accept 'sf' parameter
            # e.g., CALL dbgen(sf=1); or CALL dsdgen(sf=1);
            conn.execute(
                f"CALL {self._duckdb_generator_proc}(sf={self.scale_factor})")

            # Determine tables to export
            if hasattr(self, "_table_names") and isinstance(self._table_names, list) and self._table_names:
                table_names = list(self._table_names)
            else:
                table_names = [
                    r[0]
                    for r in conn.execute(
                        "SELECT table_name FROM information_schema.tables "
                        "WHERE table_schema = ? AND table_type = 'BASE TABLE' "
                        "ORDER BY table_name",
                        [schema],
                    ).fetchall()
                ]

            # Export each table with optimized row group size
            for tbl in table_names:
                fq_tbl = f'{schema}."{tbl}"' if schema != "main" else f'"{tbl}"'

                # Count rows
                row_count = conn.execute(
                    f"SELECT COUNT(*) FROM {fq_tbl}").fetchone()[0]
                if row_count == 0:
                    out_path = os.path.join(
                        self.target_mount_folder_path, f"{tbl}.parquet")
                    conn.execute(
                        f"COPY (SELECT * FROM {fq_tbl}) TO ? (FORMAT 'parquet', ROW_GROUP_SIZE 1)",
                        [out_path],
                    )
                    output_files.append(out_path)
                    conn.execute(f"DROP TABLE {fq_tbl}")
                    continue

                # Create sample parquet
                sample_n = min(int(100_000), row_count)
                sample_path = os.path.join(tmp_dir, f"{tbl}_sample.parquet")
                conn.execute(
                    f"COPY (SELECT * FROM {fq_tbl} LIMIT {sample_n}) TO ? (FORMAT 'parquet')",
                    [sample_path],
                )
                file_size_bytes = os.path.getsize(sample_path)
                avg_row_bytes = max(1, int(file_size_bytes / max(1, sample_n)))

                target_bytes = self.target_row_group_size_mb * 1024 * 1024
                rows_per_group = max(
                    1, int(target_bytes // max(1, avg_row_bytes)))

                out_path = os.path.join(
                    self.target_mount_folder_path, f"{tbl}.parquet")
                conn.execute(
                    f"COPY (SELECT * FROM {fq_tbl}) TO ? (FORMAT 'parquet', ROW_GROUP_SIZE {rows_per_group})",
                    [out_path],
                )
                output_files.append(out_path)

                # Cleanup per-table resources
                try:
                    os.remove(sample_path)
                except OSError:
                    pass
                conn.execute(f"DROP TABLE {fq_tbl}")

            return output_files

        finally:
            try:
                conn.close()
            except Exception:
                pass
            try:
                shutil.rmtree(tmp_dir, ignore_errors=True)
            except Exception:
                pass

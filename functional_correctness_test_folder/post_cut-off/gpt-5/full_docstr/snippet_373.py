import os
import tempfile
import shutil
from pathlib import Path
from typing import List, Optional

try:
    import duckdb
except Exception as e:
    duckdb = None


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

        if target_mount_folder_path is None:
            base = Path.cwd() / f"tpc_data_sf{scale_factor}"
        else:
            base = Path(target_mount_folder_path)

        self.target_mount_folder_path: Path = base.resolve()
        self.target_mount_folder_path.mkdir(parents=True, exist_ok=True)

    def _generate_duckdb_tables(self, conn) -> List[str]:
        """
        Subclasses must implement this method.
        It should generate the TPC tables in the given DuckDB connection
        and return the list of generated table names.
        """
        raise NotImplementedError(
            "Subclasses must implement _generate_duckdb_tables(conn) and return a list of table names."
        )

    def _estimate_avg_row_size_mb(self, conn, table: str, tmp_dir: Path, total_rows: int) -> float:
        sample_rows = max(1, min(total_rows, 100_000))
        sample_path = tmp_dir / f"{table}__sample.parquet"

        conn.execute(
            f"""
            COPY (SELECT * FROM "{table}" LIMIT {sample_rows})
            TO '{sample_path.as_posix()}'
            (FORMAT PARQUET, ROW_GROUP_SIZE {sample_rows});
            """
        )

        size_bytes = sample_path.stat().st_size
        if sample_rows == 0 or size_bytes == 0:
            return 0.0
        return float(size_bytes) / float(sample_rows) / (1024.0 * 1024.0)

    def _determine_row_group_rows(self, avg_row_size_mb: float) -> int:
        if avg_row_size_mb <= 0.0:
            return 10_000
        rows = int(self.target_row_group_size_mb / avg_row_size_mb)
        return max(1, rows)

    def _list_tables_from_return(self, maybe_tables: Optional[List[str]], conn) -> List[str]:
        if isinstance(maybe_tables, list) and all(isinstance(t, str) for t in maybe_tables):
            return maybe_tables
        # Fallback: list all non-system tables in 'main' schema
        res = conn.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'main'
              AND table_type = 'BASE TABLE'
            ORDER BY table_name;
            """
        ).fetchall()
        return [r[0] for r in res]

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
        if duckdb is None:
            raise RuntimeError(
                "duckdb is required to run TPC data generation but is not installed or failed to import")

        tmp_dir = Path(tempfile.mkdtemp(prefix="tpc_gen_"))
        conn = duckdb.connect(database=":memory:")

        created_tables: List[str] = []
        try:
            maybe_tables = self._generate_duckdb_tables(conn)
            created_tables = self._list_tables_from_return(maybe_tables, conn)

            for table in created_tables:
                # Count rows
                total_rows = conn.execute(
                    f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
                if total_rows == 0:
                    continue

                # Estimate average row size
                avg_row_size_mb = self._estimate_avg_row_size_mb(
                    conn, table, tmp_dir, total_rows)
                rows_per_group = self._determine_row_group_rows(
                    avg_row_size_mb)

                # Ensure output directory exists
                out_dir = self.target_mount_folder_path
                out_dir.mkdir(parents=True, exist_ok=True)
                out_path = out_dir / f"{table}.parquet"

                # Write full table with optimized row group size
                conn.execute(
                    f"""
                    COPY "{table}"
                    TO '{out_path.as_posix()}'
                    (FORMAT PARQUET, ROW_GROUP_SIZE {rows_per_group});
                    """
                )
        finally:
            try:
                conn.close()
            except Exception:
                pass
            try:
                shutil.rmtree(tmp_dir, ignore_errors=True)
            except Exception:
                pass

            # best-effort: nothing else to clean because DB is in-memory

import os
import math
import shutil
import logging
import tempfile
from pathlib import Path
from typing import List, Optional

try:
    import duckdb  # type: ignore
except Exception as e:
    duckdb = None  # type: ignore

logger = logging.getLogger(__name__)


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
        if duckdb is None:
            raise RuntimeError(
                "duckdb is required to run the TPC data generator but could not be imported.")
        if not isinstance(scale_factor, int) or scale_factor <= 0:
            raise ValueError("scale_factor must be a positive integer.")
        if not isinstance(target_row_group_size_mb, int) or target_row_group_size_mb <= 0:
            raise ValueError(
                "target_row_group_size_mb must be a positive integer.")

        self.scale_factor: int = scale_factor
        self.target_row_group_size_mb: int = target_row_group_size_mb
        self.extension_name: Optional[str] = getattr(
            self, "extension_name", None)
        self.generator_proc_name: Optional[str] = getattr(
            self, "generator_proc_name", None)
        self.include_tables: Optional[List[str]] = getattr(
            self, "include_tables", None)
        self.exclude_tables: Optional[List[str]] = getattr(
            self, "exclude_tables", None)

        self._user_output_root: Optional[Path] = Path(
            target_mount_folder_path).resolve() if target_mount_folder_path else None
        self.output_dir: Optional[Path] = None
        self.generated_tables: List[str] = []

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
        ext_name = self._resolve_extension_name()
        gen_proc = self._resolve_generator_proc(ext_name)
        self.output_dir = self._resolve_output_dir(ext_name, self.scale_factor)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        con = duckdb.connect()
        try:
            con.execute(f"INSTALL {ext_name};")
            con.execute(f"LOAD {ext_name};")
            con.execute(f"CALL {gen_proc}(sf={self.scale_factor});")

            tables = self._discover_tables(con)
            if self.include_tables:
                include_set = {t.lower() for t in self.include_tables}
                tables = [t for t in tables if t.lower() in include_set]
            if self.exclude_tables:
                exclude_set = {t.lower() for t in self.exclude_tables}
                tables = [t for t in tables if t.lower() not in exclude_set]
            self.generated_tables = tables

            for table in tables:
                try:
                    self._export_table(
                        con, table, self.output_dir, self.target_row_group_size_mb)
                except Exception as table_err:
                    logger.exception(
                        "Failed to export table %s: %s", table, table_err)

            self._cleanup_tables(con, tables)
        finally:
            try:
                con.close()
            except Exception:
                pass

    # ----------------------- Internal helpers -----------------------

    def _resolve_extension_name(self) -> str:
        if self.extension_name:
            return self.extension_name
        cls = self.__class__.__name__.lower()
        if "tpch" in cls:
            return "tpch"
        if "tpcds" in cls:
            return "tpcds"
        raise NotImplementedError(
            "extension_name must be provided by subclass (e.g., 'tpch' or 'tpcds').")

    def _resolve_generator_proc(self, ext_name: str) -> str:
        if self.generator_proc_name:
            return self.generator_proc_name
        if ext_name == "tpch":
            return "dbgen"
        if ext_name == "tpcds":
            return "dsdgen"
        raise NotImplementedError(
            "Unknown extension; cannot infer generator procedure.")

    def _resolve_output_dir(self, ext_name: str, scale_factor: int) -> Path:
        if self._user_output_root:
            base = self._user_output_root
        else:
            base = Path.cwd()
        return (base / f"{ext_name}-sf{scale_factor}").resolve()

    def _discover_tables(self, con: "duckdb.DuckDBPyConnection") -> List[str]:
        res = con.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = current_schema()
              AND table_type = 'BASE TABLE'
            ORDER BY table_name
            """
        ).fetchall()
        tables = [r[0] for r in res]
        # Filter out any non-TPC artifacts if present
        filtered = []
        for t in tables:
            tl = t.lower()
            if tl.startswith("duckdb_") or tl.startswith("sqlite_"):
                continue
            filtered.append(t)
        return filtered

    def _export_table(self, con: "duckdb.DuckDBPyConnection", table: str, output_root: Path, target_rg_mb: int) -> None:
        count = con.execute(
            f"SELECT COUNT(*) FROM {self._ident(table)}").fetchone()[0]
        if count == 0:
            return

        sample_rows = self._choose_sample_size(count)
        avg_row_bytes = self._estimate_avg_row_size_bytes(
            con, table, sample_rows)
        rows_per_group = self._compute_rows_per_group(
            avg_row_bytes, target_rg_mb, fallback_rows=100_000)

        table_dir = (output_root / table).resolve()
        if table_dir.exists():
            shutil.rmtree(table_dir)
        table_dir.mkdir(parents=True, exist_ok=True)

        con.execute(
            f"""
            COPY (SELECT * FROM {self._ident(table)})
            TO {self._str(table_dir.as_posix())}
            (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE {rows_per_group});
            """
        )

    def _choose_sample_size(self, total_rows: int) -> int:
        if total_rows <= 0:
            return 0
        # Aim for up to 100k sample rows to balance accuracy and speed
        return max(1, min(100_000, total_rows))

    def _estimate_avg_row_size_bytes(self, con: "duckdb.DuckDBPyConnection", table: str, sample_rows: int) -> float:
        if sample_rows <= 0:
            # Fallback to a nominal small row size if we cannot sample
            return 256.0

        tmp_dir = Path(tempfile.mkdtemp(prefix=f"tpc-sample-{table}-"))
        sample_file = tmp_dir / "sample.parquet"
        try:
            # Prefer reservoir sampling; fallback to LIMIT if not supported
            used_reservoir = True
            try:
                con.execute(
                    f"""
                    COPY (
                        SELECT * FROM {self._ident(table)} USING SAMPLE reservoir({sample_rows} rows)
                    )
                    TO {self._str(sample_file.as_posix())}
                    (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE {sample_rows});
                    """
                )
            except Exception:
                used_reservoir = False
                con.execute(
                    f"""
                    COPY (
                        SELECT * FROM {self._ident(table)} LIMIT {sample_rows}
                    )
                    TO {self._str(sample_file.as_posix())}
                    (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE {sample_rows});
                    """
                )

            written_rows = con.execute(
                f"SELECT COUNT(*) FROM read_parquet({self._str(sample_file.as_posix())})"
            ).fetchone()[0]
            if written_rows <= 0:
                return 256.0

            size_bytes = sample_file.stat().st_size
            avg_bytes = size_bytes / float(written_rows)
            # Guard against unrealistic estimates
            if not math.isfinite(avg_bytes) or avg_bytes <= 0:
                return 256.0

            return avg_bytes
        finally:
            try:
                shutil.rmtree(tmp_dir, ignore_errors=True)
            except Exception:
                pass

    def _compute_rows_per_group(self, avg_row_bytes: float, target_rg_mb: int, fallback_rows: int = 100_000) -> int:
        if not math.isfinite(avg_row_bytes) or avg_row_bytes <= 0:
            return fallback_rows
        target_bytes = target_rg_mb * 1024 * 1024
        rows = int(max(1, target_bytes // avg_row_bytes))
        # Cap to avoid extremely large row groups
        return min(rows, 5_000_000)

    def _cleanup_tables(self, con: "duckdb.DuckDBPyConnection", tables: List[str]) -> None:
        for t in tables:
            try:
                con.execute(f"DROP TABLE IF EXISTS {self._ident(t)};")
            except Exception:
                pass

    @staticmethod
    def _ident(name: str) -> str:
        # DuckDB identifiers are case-insensitive unless quoted;
        # Avoid quoting unless necessary to keep compatibility with generated TPC names.
        return name

    @staticmethod
    def _str(s: str) -> str:
        # Quote string for SQL
        return "'" + s.replace("'", "''") + "'"

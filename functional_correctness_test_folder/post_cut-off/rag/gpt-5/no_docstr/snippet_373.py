import os
import math
import shutil
import logging
import tempfile
from pathlib import Path
from typing import Iterable, List, Optional


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
                "target_row_group_size_mb must be a positive integer (MB)")

        self.scale_factor: int = scale_factor
        self.target_row_group_size_mb: int = target_row_group_size_mb
        self._sample_rows_max: int = 200_000
        self._min_rows_per_group: int = 1024

        base_dir = Path.cwd() / \
            f"tpc_sf{scale_factor}" if target_mount_folder_path is None else Path(
                target_mount_folder_path)
        base_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir: Path = base_dir

        self._logger = logging.getLogger(self.__class__.__name__)
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(
                "[%(levelname)s] %(name)s: %(message)s"))
            self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)

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
            import duckdb  # noqa: F401
        except Exception as e:
            raise ImportError(
                "duckdb is required to run the data generator") from e

        import duckdb
        con: duckdb.DuckDBPyConnection = duckdb.connect(database=":memory:")

        tmpdir_obj = tempfile.TemporaryDirectory()
        tmpdir = Path(tmpdir_obj.name)

        # Allow subclasses to install extensions, generate data, etc.
        self._prepare_duckdb(con)

        table_names = self._get_table_names(con)
        if not table_names:
            raise RuntimeError(
                "No tables found to generate. Ensure the subclass implements table generation and table listing.")

        self._logger.info(
            f"Generating Parquet for {len(table_names)} table(s) at {self.output_dir}")

        try:
            for table in table_names:
                qname = self._quote_ident(table)
                row_count = con.execute(
                    f"SELECT COUNT(*) FROM {qname}").fetchone()[0]
                if row_count == 0:
                    self._logger.warning(f"Table {table} is empty; skipping.")
                    continue

                sample_n = min(self._sample_rows_max, row_count)
                sample_path = tmpdir / f"{table}.sample.parquet"
                # Write a sample to Parquet to estimate bytes/row
                con.execute(
                    f"""
                    COPY (
                        SELECT * FROM {qname}
                        LIMIT {sample_n}
                    )
                    TO '{sample_path.as_posix()}'
                    (FORMAT PARQUET, COMPRESSION ZSTD)
                    """
                )
                sample_size_bytes = sample_path.stat().st_size
                bytes_per_row = sample_size_bytes / sample_n if sample_n > 0 else 1024.0

                target_group_bytes = self.target_row_group_size_mb * 1024 * 1024
                row_group_rows = max(self._min_rows_per_group, int(
                    target_group_bytes / max(bytes_per_row, 1)))
                row_group_rows = max(1, row_group_rows)

                # Remove old output file if it exists
                out_file = self.output_dir / f"{table}.parquet"
                if out_file.exists():
                    try:
                        out_file.unlink()
                    except Exception:
                        # If it's a directory for any reason, remove tree
                        if out_file.is_dir():
                            shutil.rmtree(out_file)
                        else:
                            raise

                self._logger.info(
                    f"Writing table {table}: {row_count} rows, ~{bytes_per_row:.1f} B/row, "
                    f"ROW_GROUP_SIZE={row_group_rows} (~{(row_group_rows*bytes_per_row)/(1024*1024):.1f} MB)"
                )

                con.execute(
                    f"""
                    COPY (
                        SELECT * FROM {qname}
                    )
                    TO '{out_file.as_posix()}'
                    (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE {row_group_rows})
                    """
                )

                try:
                    # type: ignore[arg-type]
                    sample_path.unlink(missing_ok=True)
                except Exception:
                    pass

        finally:
            # Attempt to drop generated tables and close connection
            try:
                for table in table_names:
                    try:
                        con.execute(
                            f"DROP TABLE IF EXISTS {self._quote_ident(table)}")
                    except Exception:
                        pass
                con.close()
            except Exception:
                pass
            tmpdir_obj.cleanup()

    # Methods intended to be overridden by subclasses

    def _prepare_duckdb(self, con):
        """
        Subclasses should override this method to:
        - INSTALL/LOAD the appropriate DuckDB extension (tpch/tpcds)
        - Generate all required tables at the given scale factor into the in-memory DB
        """
        raise NotImplementedError(
            "_prepare_duckdb must be implemented by subclasses (e.g., TPCHDataGenerator/TPCDSDataGenerator)"
        )

    def _get_table_names(self, con) -> List[str]:
        """
        Subclasses should override this method to return the list of table names
        generated in _prepare_duckdb.
        """
        # Allow subclasses to set an attribute instead of overriding
        names = getattr(self, "_table_names", None) or getattr(
            self, "table_names", None)
        if isinstance(names, (list, tuple)) and all(isinstance(n, str) for n in names):
            return list(names)
        raise NotImplementedError(
            "_get_table_names must be implemented by subclasses or set self._table_names (list[str])"
        )

    # Helpers

    @staticmethod
    def _quote_ident(name: str) -> str:
        if name is None:
            return '""'
        if name == "*":
            return name
        # Quote each identifier if schema.table
        parts = [p for p in name.split(".")]
        parts = [f'"{p.replace(chr(34), chr(34)*2)}"' for p in parts]
        return ".".join(parts)

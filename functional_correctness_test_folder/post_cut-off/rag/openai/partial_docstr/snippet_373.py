
import os
import pathlib
import tempfile
from typing import Iterable, Tuple

import duckdb


class _TPCDataGenerator:
    """
    Base class for TPC data generation. PLEASE DO NOT INSTANTIATE THIS CLASS DIRECTLY.
    Use the TPCHDataGenerator and TPCDSDataGenerator subclasses instead.
    """

    def __init__(
        self,
        scale_factor: int,
        target_mount_folder_path: str | pathlib.Path | None = None,
        target_row_group_size_mb: int = 128,
    ):
        """
        Initialize the TPC data generator with a scale factor.

        Parameters
        ----------
        scale_factor : int
            The scale factor for the data generation.
        target_mount_folder_path : str | pathlib.Path | None, optional
            Path to the folder where the Parquet files will be written.
            If ``None`` a temporary directory will be created.
        target_row_group_size_mb : int, optional
            Target size of a row group in megabytes.  DuckDB only allows
            specifying the number of rows per row group, so this value is
            used to estimate the optimal number of rows.
        """
        if not isinstance(scale_factor, int) or scale_factor <= 0:
            raise ValueError("scale_factor must be a positive integer")
        if not isinstance(target_row_group_size_mb, int) or target_row_group_size_mb <= 0:
            raise ValueError(
                "target_row_group_size_mb must be a positive integer")

        self.scale_factor = scale_factor
        self.target_row_group_size_mb = target_row_group_size_mb

        if target_mount_folder_path is None:
            self._temp_dir = True
            self.target_mount_folder_path = pathlib.Path(tempfile.mkdtemp())
        else:
            self._temp_dir = False
            self.target_mount_folder_path = pathlib.Path(
                target_mount_folder_path)

        self.target_mount_folder_path.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Subclasses must implement this method
    # ------------------------------------------------------------------
    def get_table_definitions(self) -> Iterable[Tuple[str, str]]:
        """
        Return an iterable of (table_name, sql_query) tuples that
        generate the tables in DuckDB.

        Subclasses should override this method to provide the
        specific SQL for each TPC table.
        """
        raise NotImplementedError(
            "Subclasses must implement get_table_definitions()"
        )

    # ------------------------------------------------------------------
    # Main data generation routine
    # ------------------------------------------------------------------
    def run(self):
        """
        Generate the TPC tables using DuckDB and write them to Parquet
        files in the target folder.  The method estimates the average
        row size from a small sample and uses that to compute the
        number of rows per row group for the final Parquet files.
        """
        con = duckdb.connect(database=":memory:")

        try:
            for table_name, sql in self.get_table_definitions():
                # ------------------------------------------------------------------
                # 1. Estimate average row size using a sample
                # ------------------------------------------------------------------
                sample_sql = f"SELECT * FROM ({sql}) AS t SAMPLE 1000"
                sample_df = con.execute(sample_sql).fetchdf()

                if sample_df.empty:
                    avg_row_size_mb = 0.0
                else:
                    # memory_usage returns bytes; convert to MB
                    avg_row_size_bytes = sample_df.memory_usage(
                        deep=True).sum() / len(sample_df)
                    avg_row_size_mb = avg_row_size_bytes / (1024**2)

                # ------------------------------------------------------------------
                # 2. Compute rows per row group
                # ------------------------------------------------------------------
                if avg_row_size_mb > 0:
                    rows_per_row_group = max(
                        1, int(self.target_row_group_size_mb / avg_row_size_mb)
                    )
                else:
                    rows_per_row_group = 1

                # ------------------------------------------------------------------
                # 3. Write the full table to Parquet
                # ------------------------------------------------------------------
                output_path = self.target_mount_folder_path / \
                    f"{table_name}.parquet"
                con.execute(sql).write_parquet(
                    str(output_path), row_group_size=rows_per_row_group
                )

        finally:
            con.close()

        # ------------------------------------------------------------------
        # 4. Clean up temporary directory if it was created
        # ------------------------------------------------------------------
        if self._temp_dir:
            # The caller may want to inspect the temp dir; we leave it.
            pass

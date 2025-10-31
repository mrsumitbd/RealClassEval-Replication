
import os
import csv
import random
import string
from pathlib import Path
from typing import List, Dict, Any


class _TPCDataGenerator:
    """
    A simple TPC data generator that creates CSV files for a subset of TPC-H tables.
    The generator writes a number of rows proportional to the provided scale factor.
    """

    # Define a minimal schema for a few TPC-H tables
    _TABLE_SCHEMAS: Dict[str, List[str]] = {
        "nation": ["nationkey", "name", "regionkey", "comment"],
        "region": ["regionkey", "name", "comment"],
        "customer": ["custkey", "name", "address", "nationkey", "phone", "acctbal", "mktsegment", "comment"],
        "orders": ["orderkey", "custkey", "orderstatus", "totalprice", "orderdate", "orderpriority", "clerk", "shippriority", "comment"],
        "lineitem": ["orderkey", "partkey", "suppkey", "linenumber", "quantity", "extendedprice", "discount", "tax", "returnflag", "linestatus", "shipdate", "commitdate", "receiptdate", "shipinstruct", "shipmode", "comment"],
        "supplier": ["suppkey", "name", "address", "nationkey", "phone", "acctbal", "comment"],
        "partsupp": ["partkey", "suppkey", "availqty", "supplycost", "comment"],
        "part": ["partkey", "name", "mfgr", "brand", "type", "size", "container", "reorderlevel", "rating", "comment"],
    }

    def __init__(
        self,
        scale_factor: int,
        target_mount_folder_path: str | Path | None = None,
        target_row_group_size_mb: int = 128,
    ):
        """
        Parameters
        ----------
        scale_factor : int
            The scale factor determines the number of rows per table.
            For each table, the number of rows will be `scale_factor * 1000`.
        target_mount_folder_path : str | Path | None, optional
            The directory where the generated data will be stored.
            If None, the current working directory is used.
        target_row_group_size_mb : int, optional
            The target size (in megabytes) for each row group (file).
            This parameter is currently not used in the simplified implementation.
        """
        if scale_factor <= 0:
            raise ValueError("scale_factor must be a positive integer")
        self.scale_factor = scale_factor
        self.target_row_group_size_mb = target_row_group_size_mb

        if target_mount_folder_path is None:
            target_mount_folder_path = Path.cwd()
        self.target_mount_folder_path = Path(
            target_mount_folder_path).expanduser().resolve()

        # Ensure the target directory exists
        self.target_mount_folder_path.mkdir(parents=True, exist_ok=True)

    def run(self) -> None:
        """
        Generate CSV files for each defined TPC-H table.
        Each file will contain `scale_factor * 1000` rows of random data.
        """
        rows_per_table = self.scale_factor * 1000
        for table_name, columns in self._TABLE_SCHEMAS.items():
            file_path = self.target_mount_folder_path / f"{table_name}.csv"
            self._write_table_csv(file_path, columns, rows_per_table)

    def _write_table_csv(self, file_path: Path, columns: List[str], num_rows: int) -> None:
        """
        Write a CSV file with random data for a given table schema.

        Parameters
        ----------
        file_path : Path
            The path to the CSV file to create.
        columns : List[str]
            The column names for the table.
        num_rows : int
            The number of rows to generate.
        """
        with file_path.open(mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            for _ in range(num_rows):
                row = self._generate_row(columns)
                writer.writerow(row)

    def _generate_row(self, columns: List[str]) -> Dict[str, Any]:
        """
        Generate a single row of random data based on column names.

        Parameters
        ----------
        columns : List[str]
            The column names for the row.

        Returns
        -------
        Dict[str, Any]
            A dictionary mapping column names to random values.
        """
        row: Dict[str, Any] = {}
        for col in columns:
            if "key" in col:
                row[col] = random.randint(1, 1000000)
            elif "name" in col:
                row[col] = self._random_string(10)
            elif "address" in col:
                row[col] = self._random_string(20)
            elif "phone" in col:
                row[col] = f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            elif "acctbal" in col:
                row[col] = round(random.uniform(-10000, 10000), 2)
            elif "mktsegment" in col:
                row[col] = random.choice(
                    ["AUTOMOBILE", "BUILDING", "FURNITURE", "HOUSEHOLD", "MACHINERY", "OTHER"])
            elif "orderstatus" in col:
                row[col] = random.choice(["F", "O", "P"])
            elif "totalprice" in col:
                row[col] = round(random.uniform(100, 100000), 2)
            elif "orderdate" in col or "shipdate" in col or "commitdate" in col or "receiptdate" in col:
                row[col] = self._random_date()
            elif "orderpriority" in col:
                row[col] = random.choice(
                    ["1-URGENT", "2-HIGH", "3-MEDIUM", "4-LOW"])
            elif "clerk" in col:
                row[col] = f"Clerk#000000{random.randint(1, 999):03d}"
            elif "shippriority" in col:
                row[col] = random.randint(0,

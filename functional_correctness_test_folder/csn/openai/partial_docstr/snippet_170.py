
import sqlite3
from contextlib import contextmanager
from typing import Any, Dict, Optional


class MetricsDAO:
    """
    Data Access Object for metrics stored in a SQLite database.
    The underlying table is expected to have the following schema:

        CREATE TABLE IF NOT EXISTS metrics (
            run_id   TEXT NOT NULL,
            metric_id TEXT NOT NULL,
            value    REAL,
            PRIMARY KEY (run_id, metric_id)
        );
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        """
        Initialize the DAO with a path to the SQLite database.
        If the database file does not exist, it will be created.
        """
        self._db_path = db_path
        self._ensure_table()

    @contextmanager
    def _connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        try:
            yield conn
        finally:
            conn.close()

    def _ensure_table(self) -> None:
        with self._connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS metrics (
                    run_id    TEXT NOT NULL,
                    metric_id TEXT NOT NULL,
                    value     REAL,
                    PRIMARY KEY (run_id, metric_id)
                );
                """
            )
            conn.commit()

    def get(self, run_id: str, metric_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single metric by run_id and metric_id.

        :param run_id: Identifier of the run.
        :param metric_id: Identifier of the metric.
        :return: A dictionary with keys 'run_id', 'metric_id', 'value' or None if not found.
        """
        with self._connection() as conn:
            cursor = conn.execute(
                """
                SELECT run_id, metric_id, value
                FROM metrics
                WHERE run_id = ? AND metric_id = ?
                """,
                (run_id, metric_id),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return {"run_id": row[0], "metric_id": row[1], "value": row[2]}

    def delete(self, run_id: str) -> int:
        """
        Delete all metrics belonging to the given run.

        :param run_id: ID of the Run that the metric belongs to.
        :return: Number of rows deleted.
        """
        with self._connection() as conn:
            cursor = conn.execute(
                """
                DELETE FROM metrics
                WHERE run_id = ?
                """,
                (run_id,),
            )
            conn.commit()
            return cursor.rowcount

    # Optional helper methods for testing and convenience

    def insert(self, run_id: str, metric_id: str, value: float) -> None:
        """
        Insert or replace a metric. Useful for setting up test data.
        """
        with self._connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO metrics (run_id, metric_id, value)
                VALUES (?, ?, ?)
                """,
                (run_id, metric_id, value),
            )
            conn.commit()

    def list_metrics(self, run_id: str) -> Dict[str, float]:
        """
        Return all metrics for a given run as a dictionary {metric_id: value}.
        """
        with self._connection() as conn:
            cursor = conn.execute(
                """
                SELECT metric_id, value
                FROM metrics
                WHERE run_id = ?
                """,
                (run_id,),
            )
            return {row[0]: row[1] for row in cursor.fetchall()}

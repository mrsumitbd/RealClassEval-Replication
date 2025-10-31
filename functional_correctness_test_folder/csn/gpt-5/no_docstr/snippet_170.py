class MetricsDAO:
    def __init__(self, db_path=":memory:"):
        import sqlite3
        self._sqlite3 = sqlite3
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._ensure_schema()

    def _ensure_schema(self):
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS metrics (
                run_id TEXT NOT NULL,
                metric_id TEXT NOT NULL,
                value REAL,
                timestamp INTEGER,
                PRIMARY KEY (run_id, metric_id)
            )
            """
        )
        self._conn.commit()

    def get(self, run_id, metric_id):
        if run_id is None or metric_id is None:
            raise ValueError("run_id and metric_id must be provided")
        cur = self._conn.execute(
            "SELECT run_id, metric_id, value, timestamp FROM metrics WHERE run_id = ? AND metric_id = ?",
            (str(run_id), str(metric_id)),
        )
        row = cur.fetchone()
        if not row:
            return None
        return {
            "run_id": row["run_id"],
            "metric_id": row["metric_id"],
            "value": row["value"],
            "timestamp": row["timestamp"],
        }

    def delete(self, run_id):
        if run_id is None:
            raise ValueError("run_id must be provided")
        cur = self._conn.execute(
            "DELETE FROM metrics WHERE run_id = ?",
            (str(run_id),),
        )
        self._conn.commit()
        return cur.rowcount

    # Optional helpers for completeness
    def upsert(self, run_id, metric_id, value=None, timestamp=None):
        self._conn.execute(
            """
            INSERT INTO metrics (run_id, metric_id, value, timestamp)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(run_id, metric_id) DO UPDATE SET
                value=excluded.value,
                timestamp=excluded.timestamp
            """,
            (str(run_id), str(metric_id), value, timestamp),
        )
        self._conn.commit()

    def close(self):
        try:
            self._conn.close()
        except Exception:
            pass

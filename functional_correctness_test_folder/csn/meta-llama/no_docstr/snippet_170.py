
class MetricsDAO:
    def __init__(self, db_connection):
        """
        Initialize the MetricsDAO class.

        Args:
        db_connection: A database connection object.
        """
        self.db_connection = db_connection

    def get(self, run_id, metric_id):
        """
        Retrieve a metric from the database.

        Args:
        run_id (int): The ID of the run.
        metric_id (int): The ID of the metric.

        Returns:
        The metric data if found, otherwise None.
        """
        query = "SELECT * FROM metrics WHERE run_id = %s AND metric_id = %s"
        cursor = self.db_connection.cursor()
        cursor.execute(query, (run_id, metric_id))
        result = cursor.fetchone()
        cursor.close()
        return result

    def delete(self, run_id):
        """
        Delete all metrics associated with a run from the database.

        Args:
        run_id (int): The ID of the run.

        Returns:
        The number of rows deleted.
        """
        query = "DELETE FROM metrics WHERE run_id = %s"
        cursor = self.db_connection.cursor()
        cursor.execute(query, (run_id,))
        self.db_connection.commit()
        rows_deleted = cursor.rowcount
        cursor.close()
        return rows_deleted

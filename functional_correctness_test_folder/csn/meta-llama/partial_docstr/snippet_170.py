
class MetricsDAO:
    def __init__(self, db_connection):
        """
        Initialize the MetricsDAO with a database connection.

        :param db_connection: A connection to the database.
        """
        self.db_connection = db_connection

    def get(self, run_id, metric_id):
        """
        Retrieve a metric by its ID and the ID of the run it belongs to.

        :param run_id: ID of the Run that the metric belongs to.
        :param metric_id: ID of the metric to be retrieved.
        :return: The metric if found, otherwise None.
        """
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM metrics WHERE run_id = ? AND id = ?"
        cursor.execute(query, (run_id, metric_id))
        row = cursor.fetchone()
        if row:
            # Assuming the columns are id, run_id, name, value
            return {
                'id': row[0],
                'run_id': row[1],
                'name': row[2],
                'value': row[3]
            }
        else:
            return None

    def delete(self, run_id):
        '''
        Delete all metrics belonging to the given run.

        :param run_id: ID of the Run that the metric belongs to.
        '''
        cursor = self.db_connection.cursor()
        query = "DELETE FROM metrics WHERE run_id = ?"
        cursor.execute(query, (run_id,))
        self.db_connection.commit()

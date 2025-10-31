
from typing import Dict, List, Optional


class RunDAO:
    def __init__(self, db_connection):
        """
        Initialize the RunDAO class.

        Args:
        db_connection: A database connection object.
        """
        self.db_connection = db_connection

    def get(self, run_id: int) -> Optional[Dict]:
        """
        Retrieve a run by its ID.

        Args:
        run_id (int): The ID of the run to retrieve.

        Returns:
        Optional[Dict]: A dictionary representing the run, or None if not found.
        """
        query = "SELECT * FROM runs WHERE id = %s"
        cursor = self.db_connection.cursor(dictionary=True)
        cursor.execute(query, (run_id,))
        return cursor.fetchone()

    def get_runs(self, sort_by: Optional[str] = None, sort_direction: Optional[str] = None, start: int = 0, limit: Optional[int] = None, query: Dict = {'type': 'and', 'filters': []}) -> List[Dict]:
        """
        Retrieve a list of runs based on the provided query and pagination parameters.

        Args:
        sort_by (Optional[str]): The column to sort by. Defaults to None.
        sort_direction (Optional[str]): The direction to sort in. Defaults to None.
        start (int): The starting index for pagination. Defaults to 0.
        limit (Optional[int]): The maximum number of results to return. Defaults to None.
        query (Dict): A dictionary representing the query filters. Defaults to {'type': 'and', 'filters': []}.

        Returns:
        List[Dict]: A list of dictionaries representing the runs.
        """
        query_str = "SELECT * FROM runs"
        conditions = []
        params = []

        if query['type'] == 'and':
            for filter in query['filters']:
                conditions.append(
                    f"{filter['column']} {filter['operator']} %s")
                params.append(filter['value'])
        elif query['type'] == 'or':
            or_conditions = []
            for filter in query['filters']:
                or_conditions.append(
                    f"{filter['column']} {filter['operator']} %s")
                params.append(filter['value'])
            conditions.append(f"({' OR '.join(or_conditions)})")

        if conditions:
            query_str += " WHERE " + " AND ".join(conditions)

        if sort_by and sort_direction:
            query_str += f" ORDER BY {sort_by} {sort_direction.upper()}"

        # Using max uint64 for "unlimited" offset
        query_str += " LIMIT %s, %s" if limit else " LIMIT %s, 18446744073709551615"
        params.extend([start, limit]) if limit else params.append(start)

        cursor = self.db_connection.cursor(dictionary=True)
        cursor.execute(query_str, params)
        return cursor.fetchall()

    def delete(self, run_id: int) -> bool:
        """
        Delete a run by its ID.

        Args:
        run_id (int): The ID of the run to delete.

        Returns:
        bool: True if the run was deleted, False otherwise.
        """
        query = "DELETE FROM runs WHERE id = %s"
        cursor = self.db_connection.cursor()
        cursor.execute(query, (run_id,))
        self.db_connection.commit()
        return cursor.rowcount > 0

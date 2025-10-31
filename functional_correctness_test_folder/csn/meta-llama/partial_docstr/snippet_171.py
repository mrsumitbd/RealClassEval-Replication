
class NotFoundError(Exception):
    pass


class DataSourceError(Exception):
    pass


class RunDAO:
    def __init__(self, db):
        """
        Initialize the RunDAO with a database connection.

        :param db: Database connection object.
        """
        self.db = db

    def get(self, run_id):
        '''
        Return the run associated with the id.
        :raise NotFoundError when not found
        '''
        run = self.db.get_run(run_id)
        if run is None:
            raise NotFoundError(f"Run with id {run_id} not found")
        return run

    def get_runs(self, sort_by=None, sort_direction=None, start=0, limit=None, query={'type': 'and', 'filters': []}):
        """
        Get a list of runs based on the given query and pagination parameters.

        :param sort_by: Field to sort by.
        :param sort_direction: Direction of sorting (asc/desc).
        :param start: Start index for pagination.
        :param limit: Maximum number of results to return.
        :param query: Query object with 'type' and 'filters'.
        :return: List of runs.
        """
        return self.db.get_runs(sort_by, sort_direction, start, limit, query)

    def delete(self, run_id):
        '''
        Delete run with the given id from the backend.
        :param run_id: Id of the run to delete.
        :raise NotImplementedError If not supported by the backend.
        :raise DataSourceError General data source error.
        :raise NotFoundError The run was not found. (Some backends may succeed
        even if the run does not exist.
        '''
        try:
            self.db.delete_run(run_id)
        except NotImplementedError:
            raise NotImplementedError(
                "Deletion is not supported by the backend")
        except Exception as e:
            raise DataSourceError("Error deleting run") from e

        # Check if the run was actually deleted
        if self.db.get_run(run_id) is not None:
            raise DataSourceError("Failed to delete run")

# Example Database class for demonstration purposes


class Database:
    def __init__(self):
        self.runs = {
            1: {"id": 1, "name": "Run 1"},
            2: {"id": 2, "name": "Run 2"},
        }

    def get_run(self, run_id):
        return self.runs.get(run_id)

    def get_runs(self, sort_by=None, sort_direction=None, start=0, limit=None, query={'type': 'and', 'filters': []}):
        runs = list(self.runs.values())
        # Implement sorting, pagination, and filtering as needed
        return runs[start:start+limit] if limit else runs[start:]

    def delete_run(self, run_id):
        if run_id not in self.runs:
            raise NotFoundError(f"Run with id {run_id} not found")
        del self.runs[run_id]


# Example usage
if __name__ == "__main__":
    db = Database()
    run_dao = RunDAO(db)

    print(run_dao.get(1))  # Get a run by id
    print(run_dao.get_runs())  # Get all runs
    run_dao.delete(1)  # Delete a run
    try:
        print(run_dao.get(1))  # Try to get a deleted run
    except NotFoundError as e:
        print(e)

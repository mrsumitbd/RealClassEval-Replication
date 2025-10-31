
class NotFoundError(Exception):
    pass


class DataSourceError(Exception):
    pass


class RunDAO:
    '''
    Interface for accessing Runs.
    Issue: https://github.com/chovanecm/sacredboard/issues/69
    '''

    def __init__(self, db):
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
        '''Return all runs that match the query.'''
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
            raise DataSourceError(f"Failed to delete run with id {run_id}")


class Database:
    def __init__(self):
        # Initialize an in-memory database for demonstration purposes
        self.runs = {
            1: {"id": 1, "name": "Run 1"},
            2: {"id": 2, "name": "Run 2"},
            3: {"id": 3, "name": "Run 3"},
        }

    def get_run(self, run_id):
        return self.runs.get(run_id)

    def get_runs(self, sort_by=None, sort_direction=None, start=0, limit=None, query={'type': 'and', 'filters': []}):
        # Simplified implementation for demonstration purposes
        runs = list(self.runs.values())
        return runs[start:start+limit if limit else len(runs)]

    def delete_run(self, run_id):
        if run_id in self.runs:
            del self.runs[run_id]
        else:
            raise NotFoundError(f"Run with id {run_id} not found")


def main():
    db = Database()
    run_dao = RunDAO(db)

    # Test get
    print(run_dao.get(1))  # Should print: {'id': 1, 'name': 'Run 1'}
    try:
        print(run_dao.get(4))  # Should raise NotFoundError
    except NotFoundError as e:
        print(e)

    # Test get_runs
    print(run_dao.get_runs())  # Should print all runs

    # Test delete
    run_dao.delete(1)
    try:
        print(run_dao.get(1))  # Should raise NotFoundError
    except NotFoundError as e:
        print(e)


if __name__ == "__main__":
    main()

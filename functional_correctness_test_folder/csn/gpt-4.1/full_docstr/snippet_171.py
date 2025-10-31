
class NotFoundError(Exception):
    pass


class DataSourceError(Exception):
    pass


class RunDAO:
    '''
    Interface for accessing Runs.
    Issue: https://github.com/chovanecm/sacredboard/issues/69
    '''

    def __init__(self):
        self._runs = {}

    def get(self, run_id):
        '''
        Return the run associated with the id.
        :raise NotFoundError when not found
        '''
        if run_id not in self._runs:
            raise NotFoundError(f"Run with id {run_id} not found.")
        return self._runs[run_id]

    def get_runs(self, sort_by=None, sort_direction=None, start=0, limit=None, query={'type': 'and', 'filters': []}):
        '''Return all runs that match the query.'''
        runs = list(self._runs.values())

        # Apply query filtering (very basic implementation)
        if query and query.get('filters'):
            def match(run):
                for f in query['filters']:
                    key = f.get('field')
                    op = f.get('op')
                    value = f.get('value')
                    if op == 'eq':
                        if run.get(key) != value:
                            return False
                    elif op == 'ne':
                        if run.get(key) == value:
                            return False
                    # Add more operators as needed
                return True
            runs = [run for run in runs if match(run)]

        # Sorting
        if sort_by:
            reverse = (sort_direction == 'desc')
            runs.sort(key=lambda x: x.get(sort_by, None), reverse=reverse)

        # Pagination
        if limit is not None:
            runs = runs[start:start+limit]
        else:
            runs = runs[start:]

        return runs

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
            if run_id not in self._runs:
                raise NotFoundError(f"Run with id {run_id} not found.")
            del self._runs[run_id]
        except NotFoundError:
            raise
        except Exception as e:
            raise DataSourceError(str(e))

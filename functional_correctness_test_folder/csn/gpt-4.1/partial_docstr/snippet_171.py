
class NotFoundError(Exception):
    pass


class DataSourceError(Exception):
    pass


class RunDAO:
    def __init__(self):
        self._runs = {}  # run_id -> run dict

    def get(self, run_id):
        '''
        Return the run associated with the id.
        :raise NotFoundError when not found
        '''
        if run_id not in self._runs:
            raise NotFoundError(f"Run with id {run_id} not found.")
        return self._runs[run_id]

    def get_runs(self, sort_by=None, sort_direction=None, start=0, limit=None, query={'type': 'and', 'filters': []}):
        # Filtering
        def match(run, query):
            if not query or 'filters' not in query or not query['filters']:
                return True
            if query['type'] == 'and':
                return all(self._filter_match(run, f) for f in query['filters'])
            elif query['type'] == 'or':
                return any(self._filter_match(run, f) for f in query['filters'])
            else:
                return True

        runs = [run for run in self._runs.values() if match(run, query)]

        # Sorting
        if sort_by:
            reverse = (sort_direction == 'desc')
            runs.sort(key=lambda r: r.get(sort_by, None), reverse=reverse)

        # Pagination
        if limit is not None:
            runs = runs[start:start+limit]
        else:
            runs = runs[start:]
        return runs

    def _filter_match(self, run, filter_):
        # filter_ is expected to be a dict like {'field': ..., 'op': ..., 'value': ...}
        field = filter_.get('field')
        op = filter_.get('op')
        value = filter_.get('value')
        run_value = run.get(field, None)
        if op == 'eq':
            return run_value == value
        elif op == 'ne':
            return run_value != value
        elif op == 'lt':
            return run_value < value
        elif op == 'le':
            return run_value <= value
        elif op == 'gt':
            return run_value > value
        elif op == 'ge':
            return run_value >= value
        elif op == 'in':
            return run_value in value
        elif op == 'notin':
            return run_value not in value
        else:
            return False

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

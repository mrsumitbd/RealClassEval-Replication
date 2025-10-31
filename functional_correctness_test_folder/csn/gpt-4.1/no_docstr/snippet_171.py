
class RunDAO:
    def __init__(self):
        self._runs = {}
        self._next_id = 1

    def get(self, run_id):
        return self._runs.get(run_id)

    def get_runs(self, sort_by=None, sort_direction=None, start=0, limit=None, query={'type': 'and', 'filters': []}):
        def match(run, query):
            if not query or 'filters' not in query or not query['filters']:
                return True
            if query['type'] == 'and':
                return all(match_filter(run, f) for f in query['filters'])
            elif query['type'] == 'or':
                return any(match_filter(run, f) for f in query['filters'])
            return True

        def match_filter(run, f):
            key = f.get('key')
            op = f.get('op')
            value = f.get('value')
            if key not in run:
                return False
            if op == 'eq':
                return run[key] == value
            elif op == 'ne':
                return run[key] != value
            elif op == 'lt':
                return run[key] < value
            elif op == 'lte':
                return run[key] <= value
            elif op == 'gt':
                return run[key] > value
            elif op == 'gte':
                return run[key] >= value
            elif op == 'in':
                return run[key] in value
            elif op == 'nin':
                return run[key] not in value
            return False

        runs = [run for run in self._runs.values() if match(run, query)]
        if sort_by:
            reverse = (sort_direction == 'desc')
            runs.sort(key=lambda x: x.get(sort_by), reverse=reverse)
        if limit is not None:
            return runs[start:start+limit]
        else:
            return runs[start:]

    def delete(self, run_id):
        if run_id in self._runs:
            del self._runs[run_id]
            return True
        return False

    # For testing: add a run
    def add(self, run):
        run_id = self._next_id
        self._next_id += 1
        run = dict(run)
        run['id'] = run_id
        self._runs[run_id] = run
        return run_id

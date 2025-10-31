class RunDAO:
    def __init__(self):
        self._runs = {}

    def get(self, run_id):
        return self._runs.get(run_id)

    def get_runs(self, sort_by=None, sort_direction=None, start=0, limit=None, query={'type': 'and', 'filters': []}):
        items = list(self._runs.values())
        if query:
            items = [it for it in items if self._match_query(it, query)]

        if sort_by:
            reverse = (str(sort_direction).lower() == 'desc')
            items.sort(key=lambda x: self._get_field(
                x, sort_by), reverse=reverse)

        if start is None or start < 0:
            start = 0
        if limit is None:
            return items[start:]
        if limit < 0:
            return []
        end = start + limit
        return items[start:end]

    def delete(self, run_id):
        if run_id in self._runs:
            del self._runs[run_id]
            return True
        return False

    # Optional helpers for managing data
    def upsert(self, run):
        run_id = run.get('id') or run.get('_id')
        if run_id is None:
            raise ValueError('run must contain id or _id')
        self._runs[run_id] = run
        return run

    # Internal helpers
    def _get_field(self, obj, dotted_key, default=None):
        parts = str(dotted_key).split('.')
        cur = obj
        for p in parts:
            if isinstance(cur, dict) and p in cur:
                cur = cur[p]
            else:
                return default
        return cur

    def _match_query(self, item, query):
        if query is None:
            return True
        qtype = str(query.get('type', 'and')).lower()
        filters = query.get('filters', [])

        if qtype == 'not':
            if not filters:
                return True
            return not self._match_query(item, filters[0] if isinstance(filters, list) else filters)

        if not isinstance(filters, list):
            filters = [filters]

        results = []
        for f in filters:
            if isinstance(f, dict) and 'type' in f and 'filters' in f:
                results.append(self._match_query(item, f))
            else:
                results.append(self._match_filter(item, f))

        if qtype == 'or':
            return any(results)
        # default to 'and'
        return all(results)

    def _match_filter(self, item, flt):
        if not isinstance(flt, dict):
            return False
        field = flt.get('field')
        op = str(flt.get('op', 'eq')).lower()
        value = flt.get('value')

        actual = self._get_field(item, field, default=None)

        try:
            if op == 'eq':
                return actual == value
            if op == 'ne':
                return actual != value
            if op == 'lt':
                return actual is not None and actual < value
            if op == 'lte':
                return actual is not None and actual <= value
            if op == 'gt':
                return actual is not None and actual > value
            if op == 'gte':
                return actual is not None and actual >= value
            if op == 'in':
                return actual in (value or [])
            if op == 'nin':
                return actual not in (value or [])
            if op == 'exists':
                return (actual is not None) if bool(value) else (actual is None)
            if op == 'contains':
                if actual is None:
                    return False
                if isinstance(actual, (list, tuple, set)):
                    return value in actual
                return str(value) in str(actual)
            if op == 'icontains':
                if actual is None:
                    return False
                return str(value).lower() in str(actual).lower()
            if op == 'startswith':
                return isinstance(actual, str) and isinstance(value, str) and actual.startswith(value)
            if op == 'istartswith':
                return isinstance(actual, str) and isinstance(value, str) and actual.lower().startswith(value.lower())
            if op == 'endswith':
                return isinstance(actual, str) and isinstance(value, str) and actual.endswith(value)
            if op == 'iendswith':
                return isinstance(actual, str) and isinstance(value, str) and actual.lower().endswith(value.lower())
        except Exception:
            return False

        return False

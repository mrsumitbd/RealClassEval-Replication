class NotFoundError(Exception):
    pass


class DataSourceError(Exception):
    pass


class RunDAO:
    def __init__(self, runs=None, id_field="id"):
        self._id_field = id_field
        self._runs = {}
        if runs:
            for run in runs:
                rid = self._extract_id(run)
                self._runs[rid] = run

    def _extract_id(self, run):
        try:
            return run[self._id_field]
        except Exception:
            raise DataSourceError(f"Run missing id field '{self._id_field}'")

    def get(self, run_id):
        '''
        Return the run associated with the id.
        :raise NotFoundError when not found
        '''
        try:
            return self._runs[run_id]
        except KeyError:
            raise NotFoundError(f"Run '{run_id}' not found")

    def get_runs(self, sort_by=None, sort_direction=None, start=0, limit=None, query={'type': 'and', 'filters': []}):
        try:
            items = list(self._runs.values())
            items = self._apply_query(
                items, query or {'type': 'and', 'filters': []})
            items = self._apply_sort(items, sort_by, sort_direction)
            if start is None or start < 0:
                start = 0
            if limit is None:
                return items[start:]
            if limit < 0:
                return []
            return items[start:start + limit]
        except NotFoundError:
            raise
        except Exception as e:
            raise DataSourceError(str(e)) from e

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
            del self._runs[run_id]
        except KeyError:
            raise NotFoundError(f"Run '{run_id}' not found")
        except Exception as e:
            raise DataSourceError(str(e)) from e

    def _apply_query(self, items, query):
        qtype = (query.get('type') or 'and').lower()
        filters = query.get('filters') or []

        if not filters:
            return items

        def match(item, flt):
            field = flt.get('field')
            op = (flt.get('op') or 'eq').lower()
            value = flt.get('value')

            present = self._get_field(item, field, missing_sentinel=object())
            exists = present is not object()

            if op == 'exists':
                return bool(value) is True and exists or (bool(value) is False and not exists)

            if not exists:
                return False

            left = present
            right = value

            try:
                if op in ('eq', '=='):
                    return left == right
                if op in ('ne', '!='):
                    return left != right
                if op in ('lt', '<'):
                    return left < right
                if op in ('lte', '<='):
                    return left <= right
                if op in ('gt', '>'):
                    return left > right
                if op in ('gte', '>='):
                    return left >= right
                if op == 'in':
                    try:
                        return left in right
                    except TypeError:
                        return False
                if op == 'nin':
                    try:
                        return left not in right
                    except TypeError:
                        return True
                if op == 'contains':
                    try:
                        return right in left
                    except TypeError:
                        return False
                if op == 'icontains':
                    try:
                        return str(right).lower() in str(left).lower()
                    except Exception:
                        return False
                if op == 'startswith':
                    try:
                        return str(left).startswith(str(right))
                    except Exception:
                        return False
                if op == 'istartswith':
                    try:
                        return str(left).lower().startswith(str(right).lower())
                    except Exception:
                        return False
                if op == 'endswith':
                    try:
                        return str(left).endswith(str(right))
                    except Exception:
                        return False
                if op == 'iendswith':
                    try:
                        return str(left).lower().endswith(str(right).lower())
                    except Exception:
                        return False
            except Exception:
                return False
            return False

        def combine(flags):
            return all(flags) if qtype == 'and' else any(flags)

        if qtype == 'not':
            return [it for it in items if not combine([match(it, f) for f in filters])]

        return [it for it in items if combine([match(it, f) for f in filters])]

    def _apply_sort(self, items, sort_by, sort_direction):
        if not sort_by:
            return items

        if isinstance(sort_by, (list, tuple)):
            fields = list(sort_by)
        else:
            fields = [sort_by]

        if sort_direction is None:
            directions = ['asc'] * len(fields)
        elif isinstance(sort_direction, (list, tuple)):
            directions = [str(d or 'asc').lower() for d in sort_direction]
            if len(directions) < len(fields):
                directions += ['asc'] * (len(fields) - len(directions))
        else:
            directions = [str(sort_direction or 'asc').lower()] * len(fields)

        def keyfunc(item):
            keys = []
            for f in fields:
                val = self._get_field(item, f, None)
                keys.append(val)
            return tuple(keys)

        # Python can't sort with per-field directions directly; apply stable sorts in reverse order
        sorted_items = items
        for field, direction in reversed(list(zip(fields, directions))):
            reverse = direction.startswith('d')  # desc
            sorted_items = sorted(sorted_items, key=lambda it: self._get_field(
                it, field, None), reverse=reverse)
        return sorted_items

    def _get_field(self, item, field, missing_sentinel=None):
        if field is None:
            return missing_sentinel
        cur = item
        try:
            for part in str(field).split('.'):
                if isinstance(cur, dict):
                    if part in cur:
                        cur = cur[part]
                    else:
                        return missing_sentinel
                else:
                    if hasattr(cur, part):
                        cur = getattr(cur, part)
                    elif isinstance(cur, (list, tuple)) and part.isdigit():
                        idx = int(part)
                        try:
                            cur = cur[idx]
                        except Exception:
                            return missing_sentinel
                    else:
                        return missing_sentinel
            return cur
        except Exception:
            return missing_sentinel

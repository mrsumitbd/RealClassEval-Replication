
class RunDAO:
    """
    A simple in-memory DAO for run objects.
    Each run is expected to be a dictionary containing at least an 'id' key.
    """

    def __init__(self, runs=None):
        """
        Initialize the DAO with an optional list of run dictionaries.
        """
        self._runs = {}
        if runs:
            for run in runs:
                if 'id' not in run:
                    raise ValueError("Each run must have an 'id' field")
                self._runs[run['id']] = run

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def get(self, run_id):
        """
        Retrieve a run by its ID.
        Returns the run dictionary or None if not found.
        """
        return self._runs.get(run_id)

    def get_runs(self, sort_by=None, sort_direction=None,
                 start=0, limit=None,
                 query={'type': 'and', 'filters': []}):
        """
        Retrieve a list of runs with optional filtering, sorting, and pagination.

        Parameters
        ----------
        sort_by : str, optional
            Field name to sort by.
        sort_direction : str, optional
            'asc' for ascending, 'desc' for descending. Defaults to ascending.
        start : int, optional
            Zero-based index of the first result to return.
        limit : int, optional
            Maximum number of results to return. If None, return all after start.
        query : dict, optional
            Dictionary with keys:
                - 'type': 'and' or 'or' (currently only 'and' is supported)
                - 'filters': list of filter dicts, each with:
                    - 'field': field name
                    - 'op': operator ('eq', 'ne', 'lt', 'lte', 'gt', 'gte',
                                 'contains', 'in', 'not_in')
                    - 'value': value to compare against

        Returns
        -------
        list of run dictionaries
        """
        # Start with all runs
        runs = list(self._runs.values())

        # Apply filtering
        if query and isinstance(query, dict):
            filters = query.get('filters', [])
            if filters:
                runs = [run for run in runs if self._matches_filters(
                    run, filters, query.get('type', 'and'))]

        # Apply sorting
        if sort_by:
            reverse = sort_direction == 'desc'
            runs.sort(key=lambda r: r.get(sort_by), reverse=reverse)

        # Apply pagination
        if start < 0:
            start = 0
        if limit is None:
            return runs[start:]
        else:
            return runs[start:start + limit]

    def delete(self, run_id):
        """
        Delete a run by its ID.
        Returns True if the run was deleted, False if it did not exist.
        """
        return self._runs.pop(run_id, None) is not None

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    def _matches_filters(self, run, filters, logic_type='and'):
        """
        Check if a run matches all (or any) of the provided filters.
        """
        if logic_type == 'and':
            return all(self._match_filter(run, f) for f in filters)
        elif logic_type == 'or':
            return any(self._match_filter(run, f) for f in filters)
        else:
            raise ValueError(f"Unsupported logic type: {logic_type}")

    def _match_filter(self, run, filter_dict):
        """
        Evaluate a single filter against a run.
        """
        field = filter_dict.get('field')
        op = filter_dict.get('op')
        value = filter_dict.get('value')

        if field not in run:
            return False

        run_value = run[field]

        if op == 'eq':
            return run_value == value
        if op == 'ne':
            return run_value != value
        if op == 'lt':
            return run_value < value
        if op == 'lte':
            return run_value <= value
        if op == 'gt':
            return run_value > value
        if op == 'gte':
            return run_value >= value
        if op == 'contains':
            return value in run_value if isinstance(run_value, (str, list, tuple, set)) else False
        if op == 'in':
            return run_value in value if isinstance(value, (list, tuple, set)) else False
        if op == 'not_in':
            return run_value not in value if isinstance(value, (list, tuple, set)) else False

        raise ValueError(f"Unsupported operator: {op}")

    # ------------------------------------------------------------------
    # Convenience methods (not part of the original skeleton)
    # ------------------------------------------------------------------
    def add(self, run):
        """
        Add a new run to the DAO.
        """
        if 'id' not in run:
            raise ValueError("Run must have an 'id' field")
        self._runs[run['id']] = run

    def update(self, run_id, updates):
        """
        Update fields of an existing run.
        """
        if run_id not in self._runs:
            raise KeyError(f"Run with id {run_id} not found")
        self._runs[run_id].update(updates)

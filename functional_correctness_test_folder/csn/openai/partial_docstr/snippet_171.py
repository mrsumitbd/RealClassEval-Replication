
# ----------------------------------------------------------------------
# Exceptions
# ----------------------------------------------------------------------
class NotFoundError(Exception):
    """Raised when a requested run cannot be found."""
    pass


class DataSourceError(Exception):
    """Raised for generic data source errors."""
    pass


# ----------------------------------------------------------------------
# RunDAO implementation
# ----------------------------------------------------------------------
class RunDAO:
    """
    A simple in‑memory DAO for run objects.

    Each run is expected to be a dictionary that contains at least an
    ``id`` key.  The DAO supports basic CRUD operations and a very
    small query language for filtering, sorting and pagination.
    """

    def __init__(self, initial_runs=None):
        """
        Create a new DAO instance.

        :param initial_runs: Optional iterable of run dictionaries.
        """
        self._runs = {}
        if initial_runs:
            for run in initial_runs:
                if "id" not in run:
                    raise ValueError("Each run must have an 'id' field")
                self._runs[run["id"]] = run

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------
    def get(self, run_id):
        """
        Return the run associated with the id.

        :raise NotFoundError when not found
        """
        try:
            return self._runs[run_id]
        except KeyError:
            raise NotFoundError(f"Run with id {run_id} not found")

    def delete(self, run_id):
        """
        Delete run with the given id from the backend.

        :param run_id: Id of the run to delete.
        :raise NotImplementedError If not supported by the backend.
        :raise DataSourceError General data source error.
        :raise NotFoundError The run was not found.
        """
        try:
            del self._runs[run_id]
        except KeyError:
            raise NotFoundError(f"Run with id {run_id} not found")

    # ------------------------------------------------------------------
    # Querying
    # ------------------------------------------------------------------
    def get_runs(
        self,
        sort_by=None,
        sort_direction=None,
        start=0,
        limit=None,
        query={"type": "and", "filters": []},
    ):
        """
        Return a list of runs that match the supplied query.

        Parameters
        ----------
        sort_by : str or None
            Field name to sort on.
        sort_direction : str or None
            'asc' or 'desc'.
        start : int
            Zero‑based index of the first result to return.
        limit : int or None
            Maximum number of results to return.
        query : dict
            Simple query structure:
                {
                    "type": "and" | "or",
                    "filters": [
                        {"field": str, "op": str, "value": any},
                        ...
                    ]
                }
            Supported ops: eq, ne, lt, lte, gt, gte, contains

        Returns
        -------
        list of run dicts
        """
        # 1. Filter
        runs = list(self._runs.values())
        if query and query.get("filters"):
            runs = self._apply_filters(runs, query)

        # 2. Sort
        if sort_by:
            reverse = sort_direction == "desc"
            runs.sort(key=lambda r: r.get(sort_by), reverse=reverse)

        # 3. Pagination
        end = None if limit is None else start + limit
        return runs[start:end]

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    def _apply_filters(self, runs, query):
        """Apply the simple filter logic to a list of runs."""
        op_funcs = {
            "eq": lambda a, b: a == b,
            "ne": lambda a, b: a != b,
            "lt": lambda a, b: a < b,
            "lte": lambda a, b: a <= b,
            "gt": lambda a, b: a > b,
            "gte": lambda a, b: a >= b,
            "contains": lambda a, b: b in a if isinstance(a, (str, list, tuple, set)) else False,
        }

        def match(run, filt):
            field = filt["field"]
            op = filt["op"]
            value = filt["value"]
            if op not in op_funcs:
                raise ValueError(f"Unsupported operator: {op}")
            return op_funcs[op](run.get(field), value)

        if query["type"] == "and":
            return [r for r in runs if all(match(r, f) for f in query["filters"])]
        elif query["type"] == "or":
            return [r for r in runs if any(match(r, f) for f in query["filters"])]
        else:
            raise ValueError(f"Unsupported query type: {query['type']}")

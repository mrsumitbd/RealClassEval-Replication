
import abc
from typing import Any, Dict, Iterable, List, Optional, Tuple


# --------------------------------------------------------------------------- #
# Exceptions
# --------------------------------------------------------------------------- #
class NotFoundError(Exception):
    """Raised when a requested run cannot be found."""
    pass


class DataSourceError(Exception):
    """Raised for generic data‑source related errors."""
    pass


# --------------------------------------------------------------------------- #
# RunDAO interface
# --------------------------------------------------------------------------- #
class RunDAO(abc.ABC):
    """
    Interface for accessing Runs.

    Issue: https://github.com/chovanecm/sacredboard/issues/69
    """

    @abc.abstractmethod
    def get(self, run_id: str) -> Dict[str, Any]:
        """
        Return the run associated with the id.

        :param run_id: Identifier of the run.
        :raises NotFoundError: When the run cannot be found.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_runs(
        self,
        sort_by: Optional[str] = None,
        sort_direction: Optional[str] = None,
        start: int = 0,
        limit: Optional[int] = None,
        query: Dict[str, Any] = None,
    ) -> Iterable[Dict[str, Any]]:
        """
        Return all runs that match the query.

        :param sort_by: Field to sort by.
        :param sort_direction: 'asc' or 'desc'.
        :param start: Zero‑based index of the first result.
        :param limit: Maximum number of results to return.
        :param query: Dictionary describing the query. Defaults to an empty
                      'and' query.
        :returns: An iterable of run dictionaries.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, run_id: str) -> None:
        """
        Delete run with the given id from the backend.

        :param run_id: Id of the run to delete.
        :raises NotImplementedError: If deletion is not supported by the backend.
        :raises DataSourceError: General data source error.
        :raises NotFoundError: The run was not found. (Some backends may succeed
                               even if the run does not exist.)
        """
        raise NotImplementedError

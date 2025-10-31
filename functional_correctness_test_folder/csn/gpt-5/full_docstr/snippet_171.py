from abc import ABC, abstractmethod


class RunDAO(ABC):
    '''
    Interface for accessing Runs.
    Issue: https://github.com/chovanecm/sacredboard/issues/69
    '''

    @abstractmethod
    def get(self, run_id):
        '''
        Return the run associated with the id.
        :raise NotFoundError when not found
        '''
        raise NotImplementedError("Subclasses must implement get(run_id)")

    @abstractmethod
    def get_runs(self, sort_by=None, sort_direction=None, start=0, limit=None, query={'type': 'and', 'filters': []}):
        '''Return all runs that match the query.'''
        raise NotImplementedError("Subclasses must implement get_runs(...)")

    @abstractmethod
    def delete(self, run_id):
        '''
        Delete run with the given id from the backend.
        :param run_id: Id of the run to delete.
        :raise NotImplementedError If not supported by the backend.
        :raise DataSourceError General data source error.
        :raise NotFoundError The run was not found. (Some backends may succeed
        even if the run does not exist.
        '''
        raise NotImplementedError("Subclasses must implement delete(run_id)")

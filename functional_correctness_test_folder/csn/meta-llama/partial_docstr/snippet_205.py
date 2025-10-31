
from sqlalchemy.orm.query import Query
from abc import ABC, abstractmethod


class ModelView:
    # Assuming ModelView is defined elsewhere
    pass


class ArgFilterBase(ABC):
    '''An abstract specification of a filter from a query argument.
    Implementing classes must provide :py:meth:`maybe_set_arg_name` and
    :py:meth:`filter_query`.
    '''
    @abstractmethod
    def maybe_set_arg_name(self, arg_name):
        pass

    @abstractmethod
    def filter_query(self, query: Query, view: ModelView, arg_value: str) -> Query:
        '''Filter the query.
        :param query: The query to filter.
        :type query: :py:class:`sqlalchemy.orm.query.Query`
        :param view: The view with the model we wish to filter for.
        :type view: :py:class:`ModelView`
        :param str arg_value: The filter specification
        :return: The filtered query
        :rtype: :py:class:`sqlalchemy.orm.query.Query`
        :raises: :py:class:`NotImplementedError` if no implementation is
            provided.
        '''
        raise NotImplementedError("Subclass must implement abstract method")

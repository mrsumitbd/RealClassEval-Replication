
from abc import ABC, abstractmethod


class BasePagination(ABC):
    """
    The base class each Pagination class should implement.
    """

    @abstractmethod
    def paginate_query(self, query, request):
        """
        :param query: SQLAlchemy ``query``.
        :param request: The request from the view
        :return: The paginated data based on the provided query and request.
        """
        pass

    @abstractmethod
    def get_paginated_response(self, data):
        """
        :param data: The paginated data to be returned in the response.
        :return: The formatted paginated response.
        """
        pass

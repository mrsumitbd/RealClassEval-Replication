
class BasePagination:
    '''
    The base class each Pagination class should implement.
    '''

    def paginate_query(self, query, request):
        '''
        :param query: SQLAlchemy ``query``.
        :param request: The request from the view
        :return: The paginated data based on the provided query and request.
        '''
        raise NotImplementedError("Subclasses must implement paginate_query()")

    def get_paginated_response(self, data):
        '''
        :param data: The paginated data.
        :return: A response containing the paginated data.
        '''
        raise NotImplementedError(
            "Subclasses must implement get_paginated_response()")

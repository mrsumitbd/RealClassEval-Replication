
class BasePagination:
    '''
    The base class each Pagination class should implement.
    '''

    def paginate_query(self, query, request):
        '''
        :param query: SQLAlchemy ``query``.
        :param request: The request from the view
        :return: The paginated date based on the provided query and request.
        '''
        pass

    def get_paginated_response(self, data):
        pass

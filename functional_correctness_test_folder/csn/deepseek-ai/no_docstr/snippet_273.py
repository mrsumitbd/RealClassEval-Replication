
class BasePagination:

    def paginate_query(self, query, request):
        raise NotImplementedError(
            "paginate_query method must be implemented in subclass")

    def get_paginated_response(self, data):
        raise NotImplementedError(
            "get_paginated_response method must be implemented in subclass")

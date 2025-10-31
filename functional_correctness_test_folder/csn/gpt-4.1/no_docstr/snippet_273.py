
class BasePagination:

    def paginate_query(self, query, request):
        """
        Paginate the query based on 'page' and 'page_size' parameters in the request.
        Returns the paginated items.
        """
        page = int(request.get('page', 1))
        page_size = int(request.get('page_size', 10))
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 10
        self.page = page
        self.page_size = page_size
        self.total = len(query)
        self.num_pages = (self.total + page_size - 1) // page_size
        start = (page - 1) * page_size
        end = start + page_size
        self.paginated_data = query[start:end]
        return self.paginated_data

    def get_paginated_response(self, data):
        """
        Returns a dictionary with paginated response metadata and data.
        """
        return {
            'count': self.total if hasattr(self, 'total') else len(data),
            'page': self.page if hasattr(self, 'page') else 1,
            'page_size': self.page_size if hasattr(self, 'page_size') else len(data),
            'num_pages': self.num_pages if hasattr(self, 'num_pages') else 1,
            'results': data
        }

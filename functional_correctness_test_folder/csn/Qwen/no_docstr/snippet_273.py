
class BasePagination:

    def paginate_query(self, query, request):
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        return query[start:end]

    def get_paginated_response(self, data):
        return {
            'count': len(data),
            'results': data
        }

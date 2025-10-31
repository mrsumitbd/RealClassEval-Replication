
from flask import jsonify, request


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
        raise NotImplementedError("Subclasses must implement this method")

    def get_paginated_response(self, data):
        '''
        :param data: The paginated data.
        :return: A response containing the paginated data.
        '''
        raise NotImplementedError("Subclasses must implement this method")


class Pagination(BasePagination):
    '''
    A simple pagination class that implements pagination based on limit and offset.
    '''

    def paginate_query(self, query, request):
        limit = request.args.get('limit', type=int, default=10)
        offset = request.args.get('offset', type=int, default=0)
        total = query.count()
        data = query.limit(limit).offset(offset).all()
        return {
            'data': data,
            'total': total,
            'limit': limit,
            'offset': offset
        }

    def get_paginated_response(self, data):
        return jsonify({
            'data': [item.to_dict() if hasattr(item, 'to_dict') else item for item in data['data']],
            'total': data['total'],
            'limit': data['limit'],
            'offset': data['offset']
        })


class PageNumberPagination(BasePagination):
    '''
    A pagination class that implements pagination based on page number and page size.
    '''

    def paginate_query(self, query, request):
        page = request.args.get('page', type=int, default=1)
        page_size = request.args.get('page_size', type=int, default=10)
        total = query.count()
        data = query.limit(page_size).offset((page - 1) * page_size).all()
        return {
            'data': data,
            'total': total,
            'page': page,
            'page_size': page_size
        }

    def get_paginated_response(self, data):
        return jsonify({
            'data': [item.to_dict() if hasattr(item, 'to_dict') else item for item in data['data']],
            'total': data['total'],
            'page': data['page'],
            'page_size': data['page_size'],
            # equivalent to math.ceil
            'total_pages': -(-data['total'] // data['page_size'])
        })

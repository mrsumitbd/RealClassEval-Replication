class BasePagination:
    '''
    The base class each Pagination class should implement.
    '''

    def __init__(
        self,
        page_param='page',
        page_size_param='page_size',
        limit_param='limit',
        offset_param='offset',
        default_page_size=20,
        max_page_size=100,
    ):
        self.page_param = page_param
        self.page_size_param = page_size_param
        self.limit_param = limit_param
        self.offset_param = offset_param
        self.default_page_size = default_page_size
        self.max_page_size = max_page_size

    def _get_query_params(self, request):
        if request is None:
            return {}
        # Common frameworks support
        for attr in ('args', 'GET', 'query_params'):
            if hasattr(request, attr):
                params = getattr(request, attr)
                try:
                    return params.to_dict(flat=True)  # werkzeug/multi-dict
                except Exception:
                    try:
                        return dict(params)
                    except Exception:
                        return params
        # If request itself is dict-like
        try:
            return dict(request)
        except Exception:
            return {}

    def _to_int(self, value, default=None):
        try:
            if value is None or value == '':
                return default
            return int(value)
        except (TypeError, ValueError):
            return default

    def _safe_count(self, query):
        try:
            # order_by(None) avoids unnecessary ORDER BY in count where possible
            q = getattr(query, 'order_by', lambda *_: query)
            return q(None).count() if getattr(query, 'order_by', None) else query.count()
        except Exception:
            return None

    def paginate_query(self, query, request):
        '''
        :param query: SQLAlchemy ``query``.
        :param request: The request from the view
        :return: (items, pagination_meta)
        '''
        params = self._get_query_params(request)

        # Determine mode: limit/offset takes precedence if provided
        has_limit_offset = any(k in params for k in (
            self.limit_param, self.offset_param))

        if has_limit_offset:
            limit = self._to_int(params.get(
                self.limit_param), self.default_page_size)
            offset = self._to_int(params.get(self.offset_param), 0)
            if limit is None or limit <= 0:
                limit = self.default_page_size
            if offset is None or offset < 0:
                offset = 0
            if self.max_page_size is not None:
                limit = min(limit, self.max_page_size)

            total = self._safe_count(query)
            items = query.limit(limit).offset(offset).all()

            pages = None
            page = None
            page_size = limit
            if total is not None and limit > 0:
                pages = (total + limit - 1) // limit
                page = (offset // limit) + 1

            meta = {
                'count': total,
                'pages': pages,
                'limit': limit,
                'offset': offset,
                'page': page,
                'page_size': page_size,
                'has_next': (total is None) or (offset + limit < total),
                'has_prev': offset > 0,
                'next_offset': (offset + limit) if (total is None or (offset + limit < total)) else None,
                'prev_offset': max(offset - limit, 0) if offset > 0 else None,
                'next_page': (page + 1) if page is not None and (total is None or (offset + limit < total)) else None,
                'prev_page': (page - 1) if page and page > 1 else None,
            }
            return items, meta

        # Page/page_size mode
        page = self._to_int(params.get(self.page_param), 1)
        page_size = self._to_int(params.get(
            self.page_size_param), self.default_page_size)

        if page is None or page <= 0:
            page = 1
        if page_size is None or page_size <= 0:
            page_size = self.default_page_size
        if self.max_page_size is not None:
            page_size = min(page_size, self.max_page_size)

        offset = (page - 1) * page_size
        total = self._safe_count(query)
        items = query.limit(page_size).offset(offset).all()

        pages = None
        if total is not None and page_size > 0:
            pages = (total + page_size - 1) // page_size

        has_next = (total is None) or (pages is not None and page < pages)
        has_prev = page > 1

        meta = {
            'count': total,
            'pages': pages,
            'page': page,
            'page_size': page_size,
            'limit': page_size,
            'offset': offset,
            'has_next': has_next,
            'has_prev': has_prev,
            'next_page': (page + 1) if has_next else None,
            'prev_page': (page - 1) if has_prev else None,
            'next_offset': (offset + page_size) if has_next else None,
            'prev_offset': (offset - page_size) if has_prev else None,
        }
        return items, meta

    def get_paginated_response(self, data):
        '''
        :param data: The paginated data.
        :return: A response containing the paginated data.
        '''
        if isinstance(data, tuple) and len(data) == 2:
            items, meta = data
            return {'results': items, 'pagination': meta}
        if isinstance(data, dict) and 'results' in data:
            return data
        return {'results': data}

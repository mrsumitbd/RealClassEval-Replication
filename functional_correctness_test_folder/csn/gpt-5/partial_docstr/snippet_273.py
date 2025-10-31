class BasePagination:
    '''
    The base class each Pagination class should implement.
    '''

    default_page_size = 20
    max_page_size = 100
    param_page = 'page'
    param_page_size = 'page_size'
    param_limit = 'limit'
    param_offset = 'offset'

    def _get_params(self, request):
        params = {}
        if request is None:
            return params

        # Try typical structures: dict-like, .args (e.g., Flask), .GET (e.g., Django)
        candidates = []
        if isinstance(request, dict):
            candidates.append(request)
        else:
            for attr in ('args', 'GET', 'params', 'query_params'):
                if hasattr(request, attr):
                    v = getattr(request, attr)
                    if isinstance(v, dict):
                        candidates.append(v)
                        break

        # Merge (last writer wins)
        for c in candidates:
            for k, v in c.items():
                params[k] = v

        return params

    def _parse_int(self, value, default, minimum=None, maximum=None):
        try:
            iv = int(value)
        except Exception:
            iv = default
        if minimum is not None and iv < minimum:
            iv = minimum
        if maximum is not None and iv > maximum:
            iv = maximum
        return iv

    def paginate_query(self, query, request):
        '''
        :param query: SQLAlchemy ``query``.
        :param request: The request from the view
        :return: The paginated data dict with items and metadata.
        '''
        params = self._get_params(request)

        # Determine mode: limit/offset takes precedence if either provided
        has_limit = self.param_limit in params and str(
            params.get(self.param_limit)).strip() != ''
        has_offset = self.param_offset in params and str(
            params.get(self.param_offset)).strip() != ''

        # Compute total count
        try:
            total = query.order_by(None).count()
        except Exception:
            total = query.count()

        if has_limit or has_offset:
            limit = self._parse_int(
                params.get(self.param_limit, self.default_page_size),
                default=self.default_page_size,
                minimum=1,
                maximum=self.max_page_size,
            )
            offset = self._parse_int(
                params.get(self.param_offset, 0),
                default=0,
                minimum=0,
            )
            paginated_q = query.limit(limit).offset(offset)
            items = paginated_q.all()
            return {
                'count': total,
                'limit': limit,
                'offset': offset,
                'results': items,
            }
        else:
            page_size = self._parse_int(
                params.get(self.param_page_size, self.default_page_size),
                default=self.default_page_size,
                minimum=1,
                maximum=self.max_page_size,
            )
            # Avoid division by zero
            page_size = max(1, page_size)

            # Total pages
            pages = (total + page_size -
                     1) // page_size if total is not None else 1
            pages = max(1, pages)

            page = self._parse_int(
                params.get(self.param_page, 1),
                default=1,
                minimum=1,
            )
            if page > pages:
                page = pages

            offset = (page - 1) * page_size
            paginated_q = query.limit(page_size).offset(offset)
            items = paginated_q.all()
            return {
                'count': total,
                'page': page,
                'page_size': page_size,
                'pages': pages,
                'results': items,
            }

    def get_paginated_response(self, data):
        return data

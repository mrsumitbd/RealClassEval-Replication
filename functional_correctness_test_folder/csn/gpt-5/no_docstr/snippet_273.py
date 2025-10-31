class BasePagination:
    def __init__(self, default_page_size=20, max_page_size=1000):
        self.default_page_size = int(
            default_page_size) if default_page_size else 20
        self.max_page_size = int(max_page_size) if max_page_size else 1000

        self.page = 1
        self.page_size = self.default_page_size
        self.total = 0
        self.total_pages = 0
        self.next_page = None
        self.previous_page = None

    def _get_params_source(self, request):
        if request is None:
            return {}
        # Dict-like
        if hasattr(request, "get") and callable(request.get):
            return request
        # Django-like
        if hasattr(request, "query_params"):
            return request.query_params
        if hasattr(request, "GET"):
            return request.GET
        # Fallback: try to treat as mapping
        try:
            _ = request.keys()
            return request
        except Exception:
            return {}

    def _to_int(self, value, default):
        try:
            return int(value)
        except Exception:
            return default

    def _materialize_sequence(self, query):
        # If it's already sliceable with len, keep it as is
        try:
            _ = len(query)  # may raise
            _ = query[0:0]  # test slicing
            return query, False
        except Exception:
            # Convert to list
            return list(query), True

    def paginate_query(self, query, request):
        params = self._get_params_source(request)
        page = self._to_int(params.get("page", None), 1)
        page_size = self._to_int(params.get(
            "page_size", None), self.default_page_size)

        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 1
        if self.max_page_size:
            page_size = min(page_size, self.max_page_size)

        seq, materialized = self._materialize_sequence(query)
        total = len(seq)

        if total == 0:
            self.page = 1
            self.page_size = page_size
            self.total = 0
            self.total_pages = 0
            self.next_page = None
            self.previous_page = None
            return [] if materialized else seq[0:0]

        total_pages = (total + page_size - 1) // page_size
        if page > total_pages:
            page = total_pages

        start = (page - 1) * page_size
        end = start + page_size

        results = seq[start:end]

        self.page = page
        self.page_size = page_size
        self.total = total
        self.total_pages = total_pages
        self.previous_page = page - 1 if page > 1 else None
        self.next_page = page + 1 if page < total_pages else None

        return results

    def get_paginated_response(self, data):
        return {
            "count": self.total,
            "total_pages": self.total_pages,
            "page": self.page,
            "page_size": self.page_size,
            "next_page": self.next_page,
            "previous_page": self.previous_page,
            "results": data,
        }

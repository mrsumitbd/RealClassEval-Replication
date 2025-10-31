
class BasePagination:
    """
    A simple pagination helper that works with SQLAlchemy query objects.
    It expects the `request` to provide `page` and `page_size` parameters
    (either as a dict or an object with a `.get()` method).
    """

    def __init__(self, default_page_size=10, max_page_size=100):
        self.default_page_size = default_page_size
        self.max_page_size = max_page_size
        self.total = 0

    def _get_param(self, request, name, default):
        """
        Retrieve a parameter from the request. Supports dicts and objects
        with a `.get()` method (e.g., Flask's request.args).
        """
        if isinstance(request, dict):
            return request.get(name, default)
        try:
            return request.get(name, default)
        except Exception:
            return default

    def paginate_query(self, query, request):
        """
        Apply pagination to a SQLAlchemy query and return the paginated
        results as a list. The total number of items is stored in
        `self.total` for later use in the response.
        """
        # Extract pagination parameters
        page = self._get_param(request, "page", 1)
        page_size = self._get_param(
            request, "page_size", self.default_page_size)

        # Ensure numeric values and enforce bounds
        try:
            page = int(page)
            if page < 1:
                page = 1
        except Exception:
            page = 1

        try:
            page_size = int(page_size)
            if page_size < 1:
                page_size = self.default_page_size
        except Exception:
            page_size = self.default_page_size

        if page_size > self.max_page_size:
            page_size = self.max_page_size

        # Compute offset and limit
        offset = (page - 1) * page_size

        # Count total items before applying limit/offset
        # Remove ordering to avoid unnecessary overhead
        count_query = query.order_by(None)
        self.total = count_query.count()

        # Apply pagination
        paginated_query = query.limit(page_size).offset(offset)

        # Execute and return results
        return paginated_query.all()

    def get_paginated_response(self, data):
        """
        Build a standard paginated response dictionary.
        """
        return {
            "count": self.total,
            "results": data,
        }

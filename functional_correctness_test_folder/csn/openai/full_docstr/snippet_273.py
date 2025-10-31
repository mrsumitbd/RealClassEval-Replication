
class BasePagination:
    """
    The base class each Pagination class should implement.
    """

    def paginate_query(self, query, request):
        """
        Paginate a SQLAlchemy query based on request parameters.

        :param query: SQLAlchemy ``query``.
        :param request: The request from the view (expects ``args`` dict).
        :return: A dict containing paginated data and metadata.
        """
        # Extract pagination parameters from the request
        try:
            page = int(request.args.get("page", 1))
        except (TypeError, ValueError):
            page = 1
        try:
            per_page = int(request.args.get("per_page", 10))
        except (TypeError, ValueError):
            per_page = 10

        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10

        # Compute total count
        total = query.count()

        # Apply limit and offset
        items = query.limit(per_page).offset((page - 1) * per_page).all()

        # Build pagination metadata
        pages = (total + per_page - 1) // per_page if per_page else 0

        return {
            "items": items,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": pages,
        }

    def get_paginated_response(self, data):
        """
        Build a response containing the paginated data.

        :param data: The paginated data dict returned by ``paginate_query``.
        :return: A dict suitable for JSON serialization.
        """
        # Prepare the response payload
        response = {
            "count": data.get("total", 0),
            "page": data.get("page", 1),
            "per_page": data.get("per_page", 10),
            "pages": data.get("pages", 0),
            "results": data.get("items", []),
        }
        return response

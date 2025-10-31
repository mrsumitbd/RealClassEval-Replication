
from collections import OrderedDict


class BasePagination:
    """
    Base pagination class.

    To be subclassed by concrete pagination classes.
    """

    def paginate_query(self, query, request):
        """
        Paginates a query based on the request.

        Args:
            query: The query to be paginated.
            request: The current request.

        Returns:
            A paginated query.
        """
        raise NotImplementedError("Subclasses must implement paginate_query")

    def get_paginated_response(self, data):
        """
        Returns a paginated response.

        Args:
            data: The data to be paginated.

        Returns:
            A paginated response.
        """
        raise NotImplementedError(
            "Subclasses must implement get_paginated_response")


class PageNumberPagination(BasePagination):
    """
    A simple page number pagination implementation.
    """

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def paginate_query(self, query, request):
        """
        Paginates a query based on the request.

        Args:
            query: The query to be paginated.
            request: The current request.

        Returns:
            A paginated query.
        """
        page_size = self.get_page_size(request)
        paginator = self.get_paginator(query, page_size)
        page_number = request.GET.get('page', 1)

        try:
            page_number = int(page_number)
        except ValueError:
            page_number = 1

        try:
            self.page = paginator.page(page_number)
        except paginator.page_does_not_exist:
            page_number = paginator.num_pages
            self.page = paginator.page(page_number)

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        """
        Returns a paginated response.

        Args:
            data: The data to be paginated.

        Returns:
            A paginated response.
        """
        return OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])

    def get_page_size(self, request):
        """
        Returns the page size.

        Args:
            request: The current request.

        Returns:
            The page size.
        """
        if self.page_size_query_param:
            try:
                return int(request.GET.get(self.page_size_query_param, self.page_size))
            except (KeyError, ValueError):
                pass

        return self.page_size

    def get_paginator(self, query, page_size):
        """
        Returns a paginator instance.

        Args:
            query: The query to be paginated.
            page_size: The page size.

        Returns:
            A paginator instance.
        """
        from django.core.paginator import Paginator
        return Paginator(query, page_size)

    def get_next_link(self):
        """
        Returns the next link.

        Returns:
            The next link.
        """
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.next_page_number()
        return self.replace_query_param(url, 'page', page_number)

    def get_previous_link(self):
        """
        Returns the previous link.

        Returns:
            The previous link.
        """
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.previous_page_number()
        return self.replace_query_param(url, 'page', page_number)

    def replace_query_param(self, url, key, val):
        """
        Replaces a query parameter in a URL.

        Args:
            url: The URL.
            key: The query parameter key.
            val: The query parameter value.

        Returns:
            The URL with the query parameter replaced.
        """
        from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
        (scheme, netloc, path, params, query, fragment) = urlparse(url)
        query_dict = parse_qs(query)
        query_dict[key] = [str(val)]
        query = urlencode(query_dict, doseq=True)
        return urlunparse((scheme, netloc, path, params, query, fragment))

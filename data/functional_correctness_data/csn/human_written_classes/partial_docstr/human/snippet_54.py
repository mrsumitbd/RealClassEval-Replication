from math import inf
from tweepy.client import Response

class Paginator:
    """Paginator(         self, method, *args, limit=inf, pagination_token=None, **kwargs     )

    :class:`Paginator` can be used to paginate for any :class:`Client`
    methods that support pagination

    .. note::

        When the returned response from the method being passed is of type
        :class:`requests.Response`, it will be deserialized in order to parse
        the pagination tokens, likely negating any potential performance
        benefits from using a :class:`requests.Response` return type.

    .. versionadded:: 4.0

    Parameters
    ----------
    method
        :class:`Client` method to paginate for
    args
        Positional arguments to pass to ``method``
    limit
        Maximum number of requests to make to the API
    pagination_token
        Pagination token to start pagination with
    kwargs
        Keyword arguments to pass to ``method``
    """

    def __init__(self, method, *args, **kwargs):
        self.method = method
        self.args = args
        self.kwargs = kwargs

    def __iter__(self):
        return PaginationIterator(self.method, *self.args, **self.kwargs)

    def __reversed__(self):
        return PaginationIterator(self.method, *self.args, reverse=True, **self.kwargs)

    def flatten(self, limit=inf):
        """Flatten paginated data

        Parameters
        ----------
        limit
            Maximum number of results to yield
        """
        if limit <= 0:
            return
        count = 0
        for response in PaginationIterator(self.method, *self.args, **self.kwargs):
            if isinstance(response, Response):
                response_data = response.data or []
            elif isinstance(response, dict):
                response_data = response.get('data', [])
            else:
                raise RuntimeError(f'Paginator.flatten does not support the {type(response)} return type for {self.method.__qualname__}')
            for data in response_data:
                yield data
                count += 1
                if count == limit:
                    return
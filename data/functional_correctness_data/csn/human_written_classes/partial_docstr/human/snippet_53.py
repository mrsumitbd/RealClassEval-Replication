from math import inf
from tweepy.errors import TweepyException

class Cursor:
    """:class:`Cursor` can be used to paginate for any :class:`API` methods that
    support pagination

    Parameters
    ----------
    method
        :class:`API` method to paginate for
    args
        Positional arguments to pass to ``method``
    kwargs
        Keyword arguments to pass to ``method``
    """

    def __init__(self, method, *args, **kwargs):
        if hasattr(method, 'pagination_mode'):
            if method.pagination_mode == 'cursor':
                self.iterator = CursorIterator(method, *args, **kwargs)
            elif method.pagination_mode == 'dm_cursor':
                self.iterator = DMCursorIterator(method, *args, **kwargs)
            elif method.pagination_mode == 'id':
                self.iterator = IdIterator(method, *args, **kwargs)
            elif method.pagination_mode == 'next':
                self.iterator = NextIterator(method, *args, **kwargs)
            elif method.pagination_mode == 'page':
                self.iterator = PageIterator(method, *args, **kwargs)
            else:
                raise TweepyException('Invalid pagination mode.')
        else:
            raise TweepyException('This method does not perform pagination')

    def pages(self, limit=inf):
        """Retrieve the page for each request

        Parameters
        ----------
        limit
            Maximum number of pages to iterate over

        Returns
        -------
        CursorIterator or DMCursorIterator or IdIterator or NextIterator or         PageIterator
            Iterator to iterate through pages
        """
        self.iterator.limit = limit
        return self.iterator

    def items(self, limit=inf):
        """Retrieve the items in each page/request

        Parameters
        ----------
        limit
            Maximum number of items to iterate over

        Returns
        -------
        ItemIterator
            Iterator to iterate through items
        """
        iterator = ItemIterator(self.iterator)
        iterator.limit = limit
        return iterator
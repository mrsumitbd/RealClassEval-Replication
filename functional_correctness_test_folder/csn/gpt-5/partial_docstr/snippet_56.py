class Collection:
    ''' Customized interface representing a collection of items.
    JPype wraps ``java.util.Collection`` as a Python collection.
    '''

    def __init__(self, iterable=()):
        self._items = list(iterable)

    def __len__(self) -> int:
        ''' Get the length of this collection.
        Use ``len(collection)`` to find the number of items in this
        collection.
        '''
        return len(self._items)

    def __delitem__(self, item):
        if isinstance(item, slice):
            del self._items[item]
            return
        if isinstance(item, int):
            del self._items[item]
            return
        try:
            idx = self._items.index(item)
        except ValueError:
            raise ValueError(f"Item not found: {item!r}")
        del self._items[idx]

    def __contains__(self, item) -> bool:
        ''' Check if this collection contains this item.
        Use ``item in collection`` to check if the item is 
        present.
        Args:
           item: is the item to check for.  This must be a Java
           object or an object which can be automatically converted
           such as a string.
        Returns:
           bool: True if the item is in the collection.
        '''
        return item in self._items

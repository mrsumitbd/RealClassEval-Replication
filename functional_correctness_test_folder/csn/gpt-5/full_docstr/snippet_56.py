class Collection:
    ''' Customized interface representing a collection of items.
    JPype wraps ``java.util.Collection`` as a Python collection.
    '''

    def __len__(self) -> int:
        ''' Get the length of this collection.
        Use ``len(collection)`` to find the number of items in this
        collection.
        '''
        size_method = getattr(self, "size", None)
        if callable(size_method):
            return int(size_method())
        items = getattr(self, "_items", None)
        if items is not None:
            return len(items)
        try:
            count = 0
            for _ in self:
                count += 1
            return count
        except Exception as exc:
            raise TypeError(
                "Length not supported for this collection") from exc

    def __delitem__(self, item):
        ''' Collections do not support remove by index. '''
        raise TypeError("Collections do not support remove by index.")

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
        contains_method = getattr(self, "contains", None)
        if callable(contains_method):
            try:
                return bool(contains_method(item))
            except Exception:
                pass
        items = getattr(self, "_items", None)
        if items is not None:
            return item in items
        try:
            for x in self:
                if x == item:
                    return True
            return False
        except Exception:
            return False

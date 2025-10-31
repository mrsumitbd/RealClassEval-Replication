
class Collection:
    ''' Customized interface representing a collection of items.
    JPype wraps ``java.util.Collection`` as a Python collection.
    '''

    def __len__(self) -> int:
        ''' Get the length of this collection.
        Use ``len(collection)`` to find the number of items in this
        collection.
        '''
        return self.size()

    def __delitem__(self, item):
        ''' Remove an item from the collection.
        Raises KeyError if the item is not present.
        '''
        removed = self.remove(item)
        if not removed:
            raise KeyError(item)

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
        return self.contains(item)

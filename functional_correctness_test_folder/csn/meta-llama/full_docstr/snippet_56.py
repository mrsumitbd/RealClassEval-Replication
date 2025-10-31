
class Collection:
    ''' Customized interface representing a collection of items.
    JPype wraps ``java.util.Collection`` as a Python collection.
    '''

    def __init__(self, java_collection):
        self._java_collection = java_collection

    def __len__(self) -> int:
        ''' Get the length of this collection.
        Use ``len(collection)`` to find the number of items in this
        collection.
        '''
        return self._java_collection.size()

    def __delitem__(self, item):
        ''' Collections do not support remove by index. '''
        raise TypeError(
            "Collections do not support remove by index. Use remove() instead.")

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
        return self._java_collection.contains(item)

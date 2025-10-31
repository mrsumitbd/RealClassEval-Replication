
class ReadOnlyResourceUpdateOperationException(Exception):
    pass


class ReadOnlyResourceMixin:
    '''
    The mixin to be used to forbid the update/delete and create operations.
    Remember the Python's MRO and place this mixin at the right place in the inheritance declaration.
    .. automethod:: create
    .. automethod:: update
    .. automethod:: delete
    '''
    @staticmethod
    def create(params, args, data):
        '''Raises exception.
        Just raises ReadOnlyResourceUpdateOperationException to indicate
        that this method is not available.
        :raises ReadOnlyResourceUpdateOperationException: when accessed
        '''
        raise ReadOnlyResourceUpdateOperationException(
            "Create operation is not available for read-only resources.")

    @staticmethod
    def update(params, args, data):
        '''Raises exception.
        Just raises ReadOnlyResourceUpdateOperationException to indicate
        that this method is not available.
        :raises ReadOnlyResourceUpdateOperationException: when accessed
        '''
        raise ReadOnlyResourceUpdateOperationException(
            "Update operation is not available for read-only resources.")

    @staticmethod
    def delete(params, args, data):
        '''Raises exception.
        Just raises ReadOnlyResourceUpdateOperationException to indicate
        that this method is not available.
        :raises ReadOnlyResourceUpdateOperationException: when accessed
        '''
        raise ReadOnlyResourceUpdateOperationException(
            "Delete operation is not available for read-only resources.")

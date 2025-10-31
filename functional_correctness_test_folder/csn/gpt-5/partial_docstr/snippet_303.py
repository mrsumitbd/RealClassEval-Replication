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
        try:
            from .exceptions import ReadOnlyResourceUpdateOperationException  # type: ignore
        except Exception:
            # type: ignore
            class ReadOnlyResourceUpdateOperationException(Exception):
                pass
        raise ReadOnlyResourceUpdateOperationException(
            "Read-only resource: create operation is not allowed")

    @staticmethod
    def update(params, args, data):
        try:
            from .exceptions import ReadOnlyResourceUpdateOperationException  # type: ignore
        except Exception:
            # type: ignore
            class ReadOnlyResourceUpdateOperationException(Exception):
                pass
        raise ReadOnlyResourceUpdateOperationException(
            "Read-only resource: update operation is not allowed")

    @staticmethod
    def delete(params, args, data):
        '''Raises exception.
        Just raises ReadOnlyResourceUpdateOperationException to indicate
        that this method is not available.
        :raises ReadOnlyResourceUpdateOperationException: when accessed
        '''
        try:
            from .exceptions import ReadOnlyResourceUpdateOperationException  # type: ignore
        except Exception:
            # type: ignore
            class ReadOnlyResourceUpdateOperationException(Exception):
                pass
        raise ReadOnlyResourceUpdateOperationException(
            "Read-only resource: delete operation is not allowed")

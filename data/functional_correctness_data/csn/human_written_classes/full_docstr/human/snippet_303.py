class ReadOnlyResourceMixin:
    """
    The mixin to be used to forbid the update/delete and create operations.
    Remember the Python's MRO and place this mixin at the right place in the inheritance declaration.

    .. automethod:: create
    .. automethod:: update
    .. automethod:: delete
    """
    OPERATION_CREATE = 'create'
    OPERATION_UPDATE = 'update'
    OPERATION_DELETE = 'delete'

    @staticmethod
    def create(params, args, data):
        """Raises exception.

        Just raises ReadOnlyResourceUpdateOperationException to indicate
        that this method is not available.

        :raises ReadOnlyResourceUpdateOperationException: when accessed
        """
        raise ReadOnlyResourceUpdateOperationException(ReadOnlyResourceMixin.OPERATION_CREATE)

    @staticmethod
    def update(params, args, data):
        """Raises exception.

        Just raises ReadOnlyResourceUpdateOperationException to indicate
        that this method is not available.

        :raises ReadOnlyResourceUpdateOperationException: when accessed
        """
        raise ReadOnlyResourceUpdateOperationException(ReadOnlyResourceMixin.OPERATION_UPDATE)

    @staticmethod
    def delete(params, args, data):
        """Raises exception.

        Just raises ReadOnlyResourceUpdateOperationException to indicate
        that this method is not available.

        :raises ReadOnlyResourceUpdateOperationException: when accessed
        """
        raise ReadOnlyResourceUpdateOperationException(ReadOnlyResourceMixin.OPERATION_DELETE)
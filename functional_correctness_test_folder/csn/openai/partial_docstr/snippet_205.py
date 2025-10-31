class ArgFilterBase:
    '''An abstract specification of a filter from a query argument.
    Implementing classes must provide :py:meth:`maybe_set_arg_name` and
    :py:meth:`filter_query`.
    '''

    def maybe_set_arg_name(self, arg_name):
        """Set the argument name for the filter.

        Implementing classes should override this method to store the
        provided ``arg_name`` if needed. The base implementation raises
        :class:`NotImplementedError` to enforce overriding.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__}.maybe_set_arg_name must be overridden"
        )

    def filter_query(self, query, view, arg_value):
        '''Filter the query.

        :param query: The query to filter.
        :type query: :py:class:`sqlalchemy.orm.query.Query`
        :param view: The view with the model we wish to filter for.
        :type view: :py:class:`ModelView`
        :param str arg_value: The filter specification
        :return: The filtered query
        :rtype: :py:class:`sqlalchemy.orm.query.Query`
        :raises: :py:class:`NotImplementedError` if no implementation is
            provided.
        '''
        raise NotImplementedError(
            f"{self.__class__.__name__}.filter_query must be overridden"
        )

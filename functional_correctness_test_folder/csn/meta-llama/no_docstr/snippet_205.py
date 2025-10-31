
class ArgFilterBase:
    """
    Base class for argument filters.
    """

    def maybe_set_arg_name(self, arg_name):
        """
        Sets the argument name if it hasn't been set already.

        Args:
            arg_name (str): The name of the argument.
        """
        if not hasattr(self, '_arg_name'):
            self._arg_name = arg_name

    def filter_query(self, query, view, arg_value):
        """
        Filters a query based on the provided argument value.

        Args:
            query: The query to be filtered.
            view: The view associated with the query.
            arg_value: The value of the argument.

        Returns:
            The filtered query.
        """
        raise NotImplementedError("Subclasses must implement filter_query")

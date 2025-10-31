
class ArgFilterBase:
    """
    Base class for argument‑based query filtering.

    Subclasses should set ``self.arg_name`` to the name of the attribute
    on the model that should be filtered.  The ``filter_query`` method
    applies the filter to a SQLAlchemy query object.
    """

    def maybe_set_arg_name(self, arg_name):
        """
        Set the attribute name to filter on if a non‑empty value is provided.

        Parameters
        ----------
        arg_name : str or None
            The name of the attribute to filter on.  If ``None`` or an empty
            string, the current ``arg_name`` is left unchanged.
        """
        if arg_name:
            self.arg_name = arg_name

    def filter_query(self, query, view, arg_value):
        """
        Apply a filter to the given query based on ``arg_value``.

        Parameters
        ----------
        query : sqlalchemy.orm.query.Query
            The query to filter.
        view : sqlalchemy.ext.declarative.api.DeclarativeMeta
            The model class that contains the attribute to filter on.
        arg_value : Any
            The value to filter by.  If ``None`` or an empty string, the
            original query is returned unchanged.  If ``arg_value`` is a
            list/tuple/set, an ``IN`` filter is applied.

        Returns
        -------
        sqlalchemy.orm.query.Query
            The filtered query.
        """
        # Do nothing if no value is provided
        if arg_value is None or (isinstance(arg_value, str) and not arg_value.strip()):
            return query

        # Resolve the attribute on the model
        try:
            column = getattr(view, self.arg_name)
        except AttributeError as exc:
            raise AttributeError(
                f"Model '{view.__name__}' has no attribute '{self.arg_name}'"
            ) from exc

        # Apply the appropriate filter
        if isinstance(arg_value, (list, tuple, set)):
            return query.filter(column.in_(arg_value))
        else:
            return query.filter(column == arg_value)

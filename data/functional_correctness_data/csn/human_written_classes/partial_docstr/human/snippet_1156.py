class LogDataChanges:
    """Context manager that observes the DataFrame of a data container for
    changes in the number of rows.

    Examples
    --------

    >>> from reda.testing.containers import get_simple_ert_container_nor
    >>> ERTContainer = get_simple_ert_container_nor()
    >>> from reda.containers.ERT import LogDataChanges
    >>> with LogDataChanges(ERTContainer):
    ...     # now change the data
    ...     ERTContainer.data.loc[0, "r"] = 22
    ...     ERTContainer.data.query("r < 10", inplace=True)
    >>> # ERTContainer.print_log()
    2... - root - INFO - Data size changed from 22 to 21

    """

    def __init__(self, container, filter_action='default', filter_query=''):
        self.container = container
        self.logger = container.logger
        self.filter_action = filter_action
        self.data_size_before = None
        self.data_size_after = None
        self.filter_query = filter_query

    def __enter__(self):
        if self.container.data is None:
            self.data_size_before = 0
        else:
            self.data_size_before = self.container.data.shape[0]
        return None

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None or exc_value is not None or traceback is not None:
            return
        self.data_size_after = self.container.data.shape[0]
        self.logger.info('Data sized changed from {0} to {1}'.format(self.data_size_before, self.data_size_after), extra={'filter_action': self.filter_action, 'df_size_before': self.data_size_before, 'df_size_after': self.data_size_after, 'filter_query': self.filter_query})
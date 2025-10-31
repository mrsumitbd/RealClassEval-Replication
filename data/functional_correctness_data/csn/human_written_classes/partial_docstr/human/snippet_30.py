class CallableSink:
    """A sink that executes a callable function for each log message.

    Parameters
    ----------
    function
        The function to call for each message.
    """

    def __init__(self, function):
        self._function = function

    def write(self, message):
        """Write a message by calling the function.

        Parameters
        ----------
        message
            The message to pass to the function.
        """
        self._function(message)

    def stop(self):
        """Stop the sink (no-op for callable sink)."""
        pass

    def tasks_to_complete(self):
        """Return list of tasks that need to be completed.

        Returns
        -------
        list
            Empty list as callable sink has no tasks.
        """
        return []
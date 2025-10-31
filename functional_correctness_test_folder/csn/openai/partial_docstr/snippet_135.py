class NoOpTraceId:
    """
    A placeholder trace ID that represents the absence of a real trace identifier.
    """

    def __init__(self):
        # No real ID is stored; use an empty string to signify "no operation".
        self._id = ""

    def to_id(self):
        """
        Convert TraceId object to a string.

        Returns:
            str: An empty string indicating that no trace ID is present.
        """
        return self._id

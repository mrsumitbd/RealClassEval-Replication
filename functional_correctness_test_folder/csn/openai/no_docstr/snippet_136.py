
import uuid


class TraceId:
    def __init__(self, id=None):
        """
        Create a new TraceId instance.

        Parameters
        ----------
        id : str or None, optional
            If provided, use this value as the trace ID. Otherwise, generate a
            new random UUID4 hex string.
        """
        if id is None:
            self._id = uuid.uuid4().hex
        else:
            self._id = str(id)

    def to_id(self):
        """
        Return the trace ID as a string.
        """
        return self._id

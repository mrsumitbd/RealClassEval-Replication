
import uuid


class TraceId:
    """
    A simple trace identifier that generates a random UUID4 value.
    """

    def __init__(self):
        """
        Generate a random trace id.
        """
        self._id = uuid.uuid4()

    def to_id(self):
        """
        Convert TraceId object to a string.
        """
        return str(self._id)

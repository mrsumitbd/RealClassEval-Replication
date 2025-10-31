
class Details:
    def __init__(self, details):
        """
        Initialize with a mapping of detail names to values.
        """
        if not isinstance(details, dict):
            raise TypeError("details must be a dict")
        self._details = dict(details)

    def __getattr__(self, attr):
        """
        Allow attribute access to the underlying details dictionary.
        """
        try:
            return self._details[attr]
        except KeyError:
            raise AttributeError(f"'Details' object has no attribute '{attr}'")

    @property
    def all(self):
        """
        Return a copy of all stored details.
        """
        return dict(self._details)

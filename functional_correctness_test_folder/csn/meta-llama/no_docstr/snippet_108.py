
class Details:

    def __init__(self, details):
        self._details = details

    def __getattr__(self, attr):
        if attr in self._details:
            return self._details[attr]
        else:
            raise AttributeError(f"'Details' object has no attribute '{attr}'")

    @property
    def all(self):
        return self._details

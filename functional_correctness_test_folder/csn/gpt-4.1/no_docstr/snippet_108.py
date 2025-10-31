
class Details:

    def __init__(self, details):
        self._details = dict(details)

    def __getattr__(self, attr):
        if attr in self._details:
            return self._details[attr]
        raise AttributeError(f"'Details' object has no attribute '{attr}'")

    @property
    def all(self):
        return self._details.copy()

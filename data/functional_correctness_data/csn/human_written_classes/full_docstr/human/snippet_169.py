class Cursor:
    """Interface that abstracts the cursor object returned from databases."""

    def __init__(self):
        """Declare a new cursor to iterate over runs."""
        pass

    def count(self):
        """Return the number of items in this cursor."""
        raise NotImplementedError()

    def __iter__(self):
        """Iterate over elements."""
        raise NotImplementedError()
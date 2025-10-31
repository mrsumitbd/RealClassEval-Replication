class IdGenerator:
    """Helper class to generate unique, sequential ids."""

    def __init__(self, prefix):
        self.counter = 0
        self.prefix = prefix

    def __next__(self):
        self.counter += 1
        return f'{self.prefix}_{self.counter}'

    def clear(self):
        self.counter = 0

    def register_id(self, id_string):
        """Register a manually assigned id as used, to avoid collisions."""
        try:
            prefix, count = id_string.rsplit('_', 1)
            count = int(count)
        except ValueError:
            pass
        else:
            if prefix == self.prefix:
                self.counter = max(count, self.counter)
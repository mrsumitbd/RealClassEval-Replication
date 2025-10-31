class Enum:
    """Map values to specific strings."""

    def __init__(self, *args, **kwargs):
        """Initialize the mapping."""
        self.val_map = dict(enumerate(args))
        self.val_map.update(zip(kwargs.values(), kwargs.keys(), strict=False))

    def __call__(self, val):
        """Map an integer to the string representation."""
        return self.val_map.get(val, f'Unknown ({val})')
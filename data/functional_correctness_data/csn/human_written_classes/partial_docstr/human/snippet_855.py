class LazyConstant:
    """
    Describes lazy or rarely changing value.

    Normally used to cache lazy / rarely changing values that are re-computed
    only on demand (e.g. in case a particular event is raised).

    """

    def __init__(self, value_provider):
        self.value_provider = value_provider
        self.value = not_computed

    def get_value(self):
        """Returns the value of the constant."""
        if self.value is not_computed:
            self.value = self.value_provider()
            if self.value is not_computed:
                return None
        return self.value

    def compute(self):
        """Computes the value. Does not look at the cache."""
        self.value = self.value_provider()
        if self.value is not_computed:
            return None
        else:
            return self.value

    def clear(self):
        self.value = not_computed
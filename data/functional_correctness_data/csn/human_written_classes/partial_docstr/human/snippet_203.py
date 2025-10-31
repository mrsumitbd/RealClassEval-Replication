class _UnknownConfigurableReference:
    """Represents a reference to an unknown configurable.

    This class acts as a substitute for `ConfigurableReference` when the selector
    doesn't match any known configurable.
    """

    def __init__(self, selector, evaluate):
        self._selector = selector.split('/')[-1]
        self._evaluate = evaluate

    @property
    def selector(self):
        return self._selector

    @property
    def evaluate(self):
        return self._evaluate

    def __deepcopy__(self, memo):
        """Dishonestly implements the __deepcopy__ special method.

        See `ConfigurableReference` above. If this method is called, it means there
        was an attempt to use this unknown configurable reference, so we throw an
        error here.

        Args:
          memo: The memoization dict (unused).

        Raises:
          ValueError: To report that there is no matching configurable.
        """
        addl_msg = '\n\n    To catch this earlier, ensure gin.finalize() is called.'
        _raise_unknown_reference_error(self, addl_msg)
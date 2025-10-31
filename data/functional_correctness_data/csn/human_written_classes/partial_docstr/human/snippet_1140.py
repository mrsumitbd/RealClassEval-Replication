class HasContext:
    """
    Mixin to provide a Context.

    Creates a `_context` member variable that can be assigned with :meth:`set_context`.

    Any state handler or transition callable that derives from this mixin will
    receive a context from its :class:`StateMachine` upon initialization (assuming the
    StateMachine was provided with a context itself).
    """

    def __init__(self) -> None:
        super(HasContext, self).__init__()
        self._context = None

    def set_context(self, new_context) -> None:
        """Assigns the new context to the member variable ``_context``."""
        self._context = new_context
        if hasattr(self, '_set_logging_context'):
            self._set_logging_context(self._context)
class ErrorConfiguration:
    """
    The configuration object for error handling.
    """

    def __init__(self, handlers=None, processors=None, use_flask_handler=False):
        self._use_flask_handler = use_flask_handler
        self._handlers = handlers if handlers is not None else []
        self._processors = processors if processors is not None else []

    @property
    def use_flask_handler(self):
        """
        In case of web requests, flasks provides a convenient way of exception
        handling. This handler shows the stack trace, etc. On the other hand         this setting will turn of ZSL's exception handling for web request.

        :return: Status
        """
        return self._use_flask_handler

    @property
    def handlers(self):
        return self._handlers

    @property
    def processors(self):
        return self._processors
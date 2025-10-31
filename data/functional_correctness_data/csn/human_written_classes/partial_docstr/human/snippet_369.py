class LoggingContext:
    """
    Optionally change the logging level and add a logging handler purely
    in the scope of the context manager:

    If you specify a level value, the logger’s level is set to that value
    in the scope of the with block covered by the context manager. If you
    specify a handler, it is added to the logger on entry to the block
    and removed on exit from the block. You can also ask the manager to
    close the handler for you on block exit - you could do this if you
    don’t need the handler any more.

    Stolen from [1]

    [1]:https://docs.python.org/3/howto/logging-cookbook.html#using-a-context-manager-for-selective-logging
    """

    def __init__(self, logger, level=None, handler=None, close=True):
        self.logger = logger
        self.level = level
        self.handler = handler
        self.close = close

    def __enter__(self):
        if self.level is not None:
            self.old_level = self.logger.level
            self.logger.setLevel(self.level)
        if self.handler and (not any((h.stream == self.handler.stream for h in self.logger.handlers))):
            self.logger.addHandler(self.handler)

    def __exit__(self, et, ev, tb):
        if self.level is not None:
            self.logger.setLevel(self.old_level)
        if self.handler:
            self.logger.removeHandler(self.handler)
        if self.handler and self.close:
            self.handler.close()
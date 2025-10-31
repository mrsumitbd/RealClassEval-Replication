
class ExceptionHandler:
    '''Base exception handler from which other may inherit.'''

    def wants(self, exc):
        '''Returns whether this handler wants to handle the exception or not.
        This base class returns True for all exceptions by default. Override in
        subclass if it wants to be more selective.
        Args:
          exc: Exception, the current exception.
        '''
        return True

    def handle(self, exc):
        '''Do something with the current exception.
        Args:
          exc: Exception, the current exception
        This method must be overridden.
        '''
        raise NotImplementedError(
            "Subclasses must implement the handle() method.")

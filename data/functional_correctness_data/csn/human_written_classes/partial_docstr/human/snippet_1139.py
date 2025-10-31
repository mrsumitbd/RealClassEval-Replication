class CanProcess:
    """
    The CanProcess class is meant as a base for all things that
    are able to process on the basis of a time delta (dt).

    The base implementation does nothing.

    There are three methods that can be implemented by sub-classes and are called in the
    process-method in this order:

        1. doBeforeProcess
        2. doProcess
        3. doAfterProcess

    The doBefore- and doAfterProcess methods are only called if a doProcess-method exists.
    """

    def __init__(self) -> None:
        super(CanProcess, self).__init__()

    def __call__(self, dt=0):
        self.process(dt)

    def process(self, dt=0) -> None:
        if hasattr(self, 'doProcess'):
            if hasattr(self, 'doBeforeProcess'):
                self.doBeforeProcess(dt)
            self.doProcess(dt)
            if hasattr(self, 'doAfterProcess'):
                self.doAfterProcess(dt)
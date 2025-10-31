class QueueState:
    """ Passed through to event loops, should be "non-zero" while queues should
    be active.
    """

    def __init__(self):
        self.active = True
        self.threads = []

    def deactivate(self):
        self.active = False

    def __nonzero__(self):
        return self.active
    __bool__ = __nonzero__

    def join(self, timeout=None):
        for t in self.threads:
            t.join(timeout)
            if t.is_alive():
                log.warn('Failed to join thread [%s].' % t)
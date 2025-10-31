import signal

class SignalHandler:
    """
    Catches SIGINT and SIGTERM in order to trigger
    graceful shutdown.
    """
    _caught: bool

    def __init__(self):
        self._running = True
        signal.signal(signal.SIGINT, self._handle)
        signal.signal(signal.SIGTERM, self._handle)

    def _handle(self, _, __):
        """
        Handles signal by setting RUNNING to false.
        """
        LOG.info('Signal received, shutting down...')
        self._running = False

    @property
    def caught(self) -> bool:
        """
        Wether the signal was caught.
        """
        return self._running
class ActiveCaptureContext:
    """This class defines an object representing an active sniffer capture.

    The object is returned by a Sniffer.start_capture() command and terminates
    the capture when the 'with' clause exits. It is syntactic sugar for
    try/finally.
    """
    _sniffer = None
    _timeout = None

    def __init__(self, sniffer, timeout=None):
        self._sniffer = sniffer
        self._timeout = timeout

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        if self._sniffer is not None:
            if self._timeout is None:
                self._sniffer.stop_capture()
            else:
                self._sniffer.wait_for_capture(self._timeout)
        self._sniffer = None
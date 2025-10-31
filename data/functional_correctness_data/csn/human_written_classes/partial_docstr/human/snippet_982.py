import signal
import os

class SignalHandler:
    """
    Catch terminate signals to allow graceful termination of run()
    """

    def __init__(self):
        self.last_signal = None
        self.received_term_signal = False
        if os.name == 'nt':
            self.term_signals = [signal.SIGINT, signal.SIGTERM]
        else:
            self.term_signals = [signal.SIGINT, signal.SIGQUIT, signal.SIGTERM]
        for signum in self.term_signals:
            signal.signal(signum, self.handler)

    def handler(self, signum, frame):
        self.last_signal = signum
        if signum in self.term_signals:
            self.received_term_signal = True
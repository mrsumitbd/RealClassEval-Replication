import signal

class timeout:
    """
    Timeout function. Use to limit matching to a certain time limit. Note that
    this works only on Unix-based systems as it uses signal.

    Usage:
        try:
            with timeout(3):
                do_stuff()
        except TimeoutError:
            do_something_else()
    """

    def __init__(self, seconds: int=1, error_message: str='Timeout'):
        """
        Args:
            seconds (int): Allowed time for function in seconds.
            error_message (str): An error message.

        """
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        """
        Args:
            signum: Return signal from call.
            frame:
        """
        raise TimeoutError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)
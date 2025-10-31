from datetime import datetime, timedelta

class Hook:
    """
    Event handler that invokes an arbitrary callback when invoked.
    If the timeout_milliseconds argument is greater than 0,
    the hook will be suspended for n milliseconds after it's being invoked.
    """

    def __init__(self, callback, timeout_milliseconds=0, *callback_args):
        self.callback = callback
        self.timeout_milliseconds = timeout_milliseconds
        self.callback_args = callback_args
        self.ready_time = datetime.now()

    def is_ready(self):
        """
        Returns whether the hook is ready to invoke its callback or not
        """
        return datetime.now() >= self.ready_time

    def invoke(self):
        """
        Run callback, optionally passing a variable number
        of arguments `callback_args`
        """
        if self.timeout_milliseconds > 0:
            self.ready_time = datetime.now() + timedelta(milliseconds=self.timeout_milliseconds)
        self.callback(self.callback_args)
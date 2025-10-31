import time
import traceback


class SessionListener:
    def __init__(self):
        self.events = []
        self.errors = []

    def callback(self, root, raw):
        event = {
            "timestamp": time.time(),
            "root": root,
            "raw": raw,
        }
        self.events.append(event)
        return event

    def errback(self, ex):
        if isinstance(ex, BaseException):
            error_text = "".join(traceback.format_exception(
                type(ex), ex, ex.__traceback__))
        else:
            error_text = str(ex)
        error_entry = {
            "timestamp": time.time(),
            "error": error_text,
            "exception": ex,
        }
        self.errors.append(error_entry)
        return error_entry

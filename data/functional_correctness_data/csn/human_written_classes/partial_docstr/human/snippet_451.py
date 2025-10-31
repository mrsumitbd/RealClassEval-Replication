import copy
import logging
import traceback
from mobly import signals

class ExceptionRecord:
    """A record representing exception objects in TestResultRecord.

    Attributes:
      exception: Exception object, the original Exception.
      type: string, type name of the exception object.
      stacktrace: string, stacktrace of the Exception.
      extras: optional serializable, this corresponds to the
        `TestSignal.extras` field.
      position: string, an optional label specifying the position where the
        Exception ocurred.
    """

    def __init__(self, e, position=None):
        self.exception = e
        self.type = type(e).__name__
        self.stacktrace = None
        self.extras = None
        self.position = position
        self.is_test_signal = isinstance(e, signals.TestSignal)
        exc_traceback = e.__traceback__
        if exc_traceback:
            self.stacktrace = ''.join(traceback.format_exception(e.__class__, e, exc_traceback))
        if self.is_test_signal:
            self._set_details(e.details)
            self.extras = e.extras
        else:
            self._set_details(e)

    def _set_details(self, content):
        """Sets the `details` field.

        Args:
          content: the content to extract details from.
        """
        try:
            self.details = str(content)
        except UnicodeEncodeError:
            logging.error('Unable to decode "%s" in Py3, encoding in utf-8.', content)
            self.details = content.encode('utf-8')

    def to_dict(self):
        result = {}
        result[TestResultEnums.RECORD_DETAILS] = self.details
        result[TestResultEnums.RECORD_POSITION] = self.position
        result[TestResultEnums.RECORD_STACKTRACE] = self.stacktrace
        result[TestResultEnums.RECORD_EXTRAS] = copy.deepcopy(self.extras)
        return result

    def __deepcopy__(self, memo):
        """Overrides deepcopy for the class.

        If the exception object has a constructor that takes extra args, deep
        copy won't work. So we need to have a custom logic for deepcopy.
        """
        try:
            exception = copy.deepcopy(self.exception)
        except (TypeError, RecursionError):
            exception = self.exception
        result = ExceptionRecord(exception, self.position)
        result.stacktrace = self.stacktrace
        result.details = self.details
        result.extras = copy.deepcopy(self.extras)
        result.position = self.position
        return result
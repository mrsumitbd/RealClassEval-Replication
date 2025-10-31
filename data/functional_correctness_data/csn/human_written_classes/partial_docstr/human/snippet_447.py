import re
from mobly import signals

class _AssertRaisesContext:
    """A context manager used to implement TestCase.assertRaises* methods."""

    def __init__(self, expected, expected_regexp=None, extras=None):
        self.expected = expected
        self.failureException = signals.TestFailure
        self.expected_regexp = expected_regexp
        self.extras = extras

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            try:
                exc_name = self.expected.__name__
            except AttributeError:
                exc_name = str(self.expected)
            raise signals.TestFailure('%s not raised' % exc_name, extras=self.extras)
        if not issubclass(exc_type, self.expected):
            return False
        self.exception = exc_value
        if self.expected_regexp is None:
            return True
        expected_regexp = self.expected_regexp
        if isinstance(expected_regexp, str):
            expected_regexp = re.compile(expected_regexp)
        if not expected_regexp.search(str(exc_value)):
            raise signals.TestFailure('"%s" does not match "%s"' % (expected_regexp.pattern, str(exc_value)), extras=self.extras)
        return True
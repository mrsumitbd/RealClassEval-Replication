import sys
from io import StringIO

class HiddenPrints:
    """
    | Suppress console stdout prints, i.e. redirect them to a temporary string object.
    | Adapted from https://stackoverflow.com/questions/8391411/suppress-calls-to-print-python

    Examples
    --------
    >>> with HiddenPrints():
    >>>     print('foobar')
    >>> print('foobar')
    """

    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = StringIO()

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._original_stdout
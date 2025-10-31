import re
from abc import ABCMeta, abstractmethod

class Redactor:
    __slots__ = ('regex',)

    def __init__(self, regex):
        """
        Args:
            regex: What parts of the field to redact.
        """
        self.regex = regex

    @abstractmethod
    def apply(self, val):
        """Redacts information from annotated field.
        Returns: A redacted version of the string provided.
        """

    def _get_matches(self, val):
        if not self.regex:
            return None
        try:
            return re.search(self.regex, val)
        except TypeError:
            return None
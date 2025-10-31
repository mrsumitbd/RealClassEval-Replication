import collections
import traceback
import sys

class DebugHelper:

    def __init__(self):
        self._reports = []

    def add_exception(self, column, e=None):
        msg = '> An error while retrieving `{column}`: {e}'.format(column=column, e=str(e))
        self._reports.append((msg, e))

    def _write(self, msg):
        sys.stderr.write(msg)
        sys.stderr.write('\n')

    def report_summary(self, concise=True):
        _seen_messages = collections.defaultdict(int)
        for msg, e in self._reports:
            if msg not in _seen_messages or not concise:
                self._write(msg)
                self._write(''.join(traceback.format_exception(None, e, e.__traceback__)))
            _seen_messages[msg] += 1
        if concise:
            for msg, value in _seen_messages.items():
                self._write('{msg} -> Total {value} occurrences.'.format(msg=msg, value=value))
            self._write('')
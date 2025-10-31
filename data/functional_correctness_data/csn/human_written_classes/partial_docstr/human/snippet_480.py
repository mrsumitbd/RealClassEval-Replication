import pprint
import textwrap
import inspect

class Echo:
    """Context maganger for echoing variable assignments (in CPython)"""

    def __init__(self, msg, indent='  '):
        self.msg = msg
        self.indent = indent
        self.parent_frame = inspect.currentframe().f_back

    def __enter__(self):
        print(self.msg)
        self.locals_on_entry = self.parent_frame.f_locals.copy()

    def __exit__(self, exc_t, exc_v, tb):
        new_locals = dict(((k, v) for k, v in self.parent_frame.f_locals.items() if k not in self.locals_on_entry))
        print(textwrap.indent(pprint.pformat(new_locals), self.indent))
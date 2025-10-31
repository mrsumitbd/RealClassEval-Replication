import code
import sys

class Console:
    """An interactive console."""

    def __init__(self, app, globals=None, locals=None):
        self._app = app
        if locals is None:
            locals = {}
        if globals is None:
            globals = {}
        self._ipy = _InteractiveConsole(app, globals, locals)

    def eval(self, code):
        _local._current_ipy = self._ipy
        old_sys_stdout = sys.stdout
        try:
            return self._ipy.runsource(code)
        finally:
            sys.stdout = old_sys_stdout
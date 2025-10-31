from trepan.lib import breakpoint, default

class MockDebugger:

    def __init__(self):
        self.intf = [MockUserInterface()]
        self.core = MockDebuggerCore(self)
        self.settings = default.DEBUGGER_SETTINGS
        self.settings['highlight'] = None
        self.orig_sys_argv = None
        self.program_sys_argv = []
        self.eval_string = None
        return

    def stop(self):
        pass

    def restart_argv(self):
        return []
    pass
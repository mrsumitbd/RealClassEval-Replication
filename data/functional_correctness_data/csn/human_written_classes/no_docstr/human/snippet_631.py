class MockProcessor:

    def __init__(self, core):
        self.core = core
        self.debugger = core.debugger
        self.continue_running = False
        self.curframe = None
        self.event2short = {}
        self.frame = None
        self.intf = core.debugger.intf
        self.last_command = None
        self.stack = []
        return

    def get_int(self, arg, min_value=0, default=1, cmdname=None, at_most=None):
        return None

    def undefined_cmd(self, cmd):
        self.intf[-1].errmsg('Undefined mock command: "%s' % cmd)
        return
    pass
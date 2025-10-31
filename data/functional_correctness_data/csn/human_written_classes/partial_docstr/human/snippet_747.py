class SigHandler:
    """Store information about what we do when we handle a signal,

    - Do we print/not print when signal is caught
    - Do we pass/not pass the signal to the program
    - Do we stop/not stop when signal is caught

    Parameters:
       signame : name of signal (e.g. SIGUSR1 or USR1)
       print_method routine to use for "print"
       stop routine to call to invoke debugger when stopping
       pass_along: True is signal is to be passed to user's handler
    """

    def __init__(self, dbgr, signame, signum, old_handler, print_method, b_stop, print_stack=False, pass_along=True):
        self.dbgr = dbgr
        self.old_handler = old_handler
        self.pass_along = pass_along
        self.print_method = print_method
        self.print_stack = print_stack
        self.signame = signame
        self.signum = signum
        self.b_stop = b_stop
        return

    def handle(self, signum, frame):
        """This method is called when a signal is received."""
        if self.print_method:
            self.print_method(f'\n(trepan3k) Program received signal {self.signame}.')
        if self.print_stack:
            import traceback
            strings = traceback.format_stack(frame)
            for s in strings:
                if s[-1] == '\n':
                    s = s[0:-1]
                self.print_method(s)
                pass
            pass
        if self.b_stop:
            core = self.dbgr.core
            old_trace_hook_suspend = core.trace_hook_suspend
            core.trace_hook_suspend = True
            core.stop_reason = f'intercepting signal {self.signame} ({signum})'
            core.processor.event_processor(frame, 'signal', signum)
            core.trace_hook_suspend = old_trace_hook_suspend
            pass
        if self.pass_along:
            if self.old_handler:
                self.old_handler(signum, frame)
                pass
            pass
        return
    pass
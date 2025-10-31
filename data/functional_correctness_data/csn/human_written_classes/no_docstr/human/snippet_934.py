import asyncio
import logging
import functools
import time

class CallLater:
    called = False
    partial_func = None
    timer_handle = None

    def __init__(self, func, delay, loop=None, *args, **kwargs):
        self.log = logging.getLogger(type(self).__name__)
        self.func = func
        self.args = args
        self.delay = delay
        if loop:
            self.event_loop = loop
        else:
            self.event_loop = asyncio.get_event_loop()
        self.kwargs = kwargs
        self.name = f'{self.func.__name__}_{int(time.time())}'

    def schedule(self):
        self.log.debug(f'Scheduling func {self.name}')
        self.partial_func = functools.partial(self.func, *self.args, **self.kwargs)
        self.timer_handle = self.event_loop.call_later(self.delay, self.run_and_update_status)

    def run_and_update_status(self):
        self.partial_func()
        self.called = True

    def cancel(self):
        self.timer_handle.cancel()
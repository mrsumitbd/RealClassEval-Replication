from typing import Callable, Any
import threading

class Waiter:
    """
    Waits for a specified event to occur
    """

    def __init__(self, raw_key, modifiers, button, check: Callable[[Any, str, list, str], bool], name: str, time_out):
        self.raw_key = raw_key
        self.modifiers = modifiers
        self.button = button
        self.event = threading.Event()
        self.check = check
        self.name = name
        self.time_out = time_out
        self.result = ''
        if modifiers is not None:
            self.modifiers.sort()

    def wait(self):
        return self.event.wait(self.time_out)

    def handle_keypress(self, raw_key, modifiers, key, *args):
        if raw_key == self.raw_key and modifiers == self.modifiers or (self.check is not None and self.check(self, raw_key, modifiers, key, *args)):
            self.event.set()

    def handle_mouseclick(self, root_x, root_y, rel_x, rel_y, button, window_info):
        if button == self.button:
            self.event.set()
from typing import Any, Literal
import threading
from nova_act.util.terminal_manager import TerminalInputManager
import time

class KeyboardEventWatcher:
    """
    Helper class for allowing user keystrokes to be monitored on a non-blocking thread.

    Use as follows:

    with KeyboardEventWatcher("<key(s) to watch>", "<message>") as watcher:
        if watcher.is_triggered():
            do_something()
        watcher.reset()  # if you need to reuse the watcher
    """
    key: str
    trigger: threading.Event
    watcher_thread: threading.Thread | None
    final_stop: bool
    terminal_manager: TerminalInputManager

    def __init__(self, key: str, human_readable_key: str, message: str):
        self.key = key
        self.trigger = threading.Event()
        self.final_stop = False
        self.watcher_thread = None

    def _watch_for_trigger(self) -> None:
        while not self.final_stop:
            if DEBUGGER_ATTACHED_EVENT.is_set():
                _LOGGER.warning(f'Detected attached debugger; disabling {type(self).__name__}')
                self.final_stop = True
                break
            key = self.terminal_manager.get_char(block=False)
            if self.key == key:
                if self.trigger.is_set():
                    continue
                self.trigger.set()
            time.sleep(0.1)

    def __enter__(self) -> 'KeyboardEventWatcher':
        """Override terminal and start new thread when watcher is entered."""
        self.terminal_manager = TerminalInputManager().__enter__()
        self.watcher_thread = threading.Thread(target=self._watch_for_trigger, daemon=True)
        self.watcher_thread.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Literal[False]:
        """Clean up the watcher thread and reset terminal when exiting the context."""
        if self.terminal_manager:
            self.terminal_manager.__exit__(exc_type, exc_val, exc_tb)
        self.final_stop = True
        if self.watcher_thread and self.watcher_thread.is_alive():
            self.watcher_thread.join()
        return False

    def is_triggered(self) -> bool:
        return self.trigger.is_set()

    def reset(self) -> None:
        self.trigger.clear()
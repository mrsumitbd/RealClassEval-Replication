import threading
import time

class Spinner:
    """Simple loading spinner similar to UV's style."""

    def __init__(self, message: str='Loading'):
        self.message = message
        self.running = False
        self.thread = None
        self.frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.current = 0

    def start(self):
        """Start the spinner."""
        self.running = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.daemon = True
        self.thread.start()

    def _spin(self):
        """Spin animation loop."""
        while self.running:
            frame = self.frames[self.current % len(self.frames)]
            print(f'\r{frame} {self.message}...', end='', flush=True)
            self.current += 1
            time.sleep(0.1)

    def stop(self, success_message=None):
        """Stop the spinner and optionally print success message."""
        self.running = False
        if self.thread:
            self.thread.join()
        if success_message:
            print(f'\r✓ {success_message}        ')
        else:
            print('\r' + ' ' * (len(self.message) + 10), end='\r')
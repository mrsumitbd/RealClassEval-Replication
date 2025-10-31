import sys
import logging
import signal
import atexit

class CleanupManager:
    """Manages cleanup operations for the EVM environment"""

    def __init__(self):
        self.cleanup_functions = []
        self.logger = logging.getLogger(__name__)
        self._setup_handlers()

    def _setup_handlers(self):
        """Setup cleanup handlers for various exit scenarios"""
        atexit.register(self._execute_cleanup)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        if hasattr(signal, 'SIGBREAK'):
            signal.signal(signal.SIGBREAK, self._signal_handler)

    def register_cleanup(self, cleanup_func, *args, **kwargs):
        """Register a cleanup function to be called on exit"""
        self.cleanup_functions.append((cleanup_func, args, kwargs))

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f'\nReceived signal {signum}, shutting down gracefully...')
        self._execute_cleanup()
        sys.exit(0)

    def _execute_cleanup(self):
        """Execute all registered cleanup functions"""
        for cleanup_func, args, kwargs in self.cleanup_functions:
            try:
                cleanup_func(*args, **kwargs)
            except Exception as e:
                print(f'Error during cleanup: {e}')
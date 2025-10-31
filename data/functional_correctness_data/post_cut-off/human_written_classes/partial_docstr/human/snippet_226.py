from typing import Any, Callable, Dict, List, Optional, Type
import dill
from pathlib import Path
import os

class ReplState:
    """Manages persistent Python REPL state."""

    def __init__(self) -> None:
        self._namespace = {'__name__': '__main__'}
        self.persistence_dir = os.path.join(Path.cwd(), 'repl_state')
        os.makedirs(self.persistence_dir, exist_ok=True)
        self.state_file = os.path.join(self.persistence_dir, 'repl_state.pkl')
        self.load_state()

    def load_state(self) -> None:
        """Load persisted state with reset on failure."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'rb') as f:
                    saved_state = dill.load(f)
                self._namespace.update(saved_state)
                logger.debug('Successfully loaded REPL state')
            except Exception as e:
                logger.debug(f'Error loading state: {e}. Removing corrupted state file.')
                try:
                    os.remove(self.state_file)
                    logger.debug('Removed corrupted state file')
                except Exception as remove_error:
                    logger.debug(f'Error removing state file: {remove_error}')
                logger.debug('Initializing fresh REPL state')

    def save_state(self, code: Optional[str]=None) -> None:
        """Save current state."""
        try:
            if code:
                exec(code, self._namespace)
            save_dict = {}
            for name, value in self._namespace.items():
                if not name.startswith('_'):
                    try:
                        dill.dumps(value)
                        save_dict[name] = value
                    except BaseException:
                        continue
            with open(self.state_file, 'wb') as f:
                dill.dump(save_dict, f)
            logger.debug('Successfully saved REPL state')
        except Exception as e:
            logger.error(f'Error saving state: {e}')

    def execute(self, code: str) -> None:
        """Execute code and save state."""
        exec(code, self._namespace)
        self.save_state()

    def get_namespace(self) -> dict:
        """Get current namespace."""
        return dict(self._namespace)

    def clear_state(self) -> None:
        """Clear the current state and remove state file."""
        try:
            self._namespace = {'__name__': '__main__'}
            if os.path.exists(self.state_file):
                os.remove(self.state_file)
                logger.info('REPL state cleared and file removed')
            self.save_state()
        except Exception as e:
            logger.error(f'Error clearing state: {e}')

    def get_user_objects(self) -> Dict[str, str]:
        """Get user-defined objects for display."""
        objects = {}
        for name, value in self._namespace.items():
            if name.startswith('_'):
                continue
            if isinstance(value, (int, float, str, bool)):
                objects[name] = repr(value)
        return objects
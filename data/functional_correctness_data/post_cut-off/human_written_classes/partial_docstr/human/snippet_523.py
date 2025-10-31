from typing import Callable, List, Any, Optional, Dict
from fletx.utils import get_logger

class Effect:
    """
    Represents an individual effect
    A single effect that can be executed, 
    with its own dependencies, execution function, 
    and identification key, allowing to manage effects 
    in a precise and isolated way.
    """

    def __init__(self, effect_fn: Callable, dependencies: List[Any]=None):
        self.effect_fn = effect_fn
        self.dependencies = dependencies
        self._cleanup_fn = None
        self._last_deps = None
        self._logger = get_logger('FletX.Effect')

    @classmethod
    @property
    def logger(cls):
        if not cls._logger:
            cls._logger = get_logger('FletX.Effect')
        return cls._logger

    def run(self):
        """Runs the effect if dependencies have changed"""
        should_run = self.dependencies is None or self._last_deps is None or any((dep != last for dep, last in zip(self.dependencies, self._last_deps)))
        if should_run:
            if self._cleanup_fn:
                try:
                    self._cleanup_fn()
                except Exception as e:
                    self.logger.error(f'Cleanup error: {e}', exc_info=True)
            result = self.effect_fn()
            if callable(result):
                self._cleanup_fn = result
            else:
                self._cleanup_fn = None
            if self.dependencies is not None:
                self._last_deps = self.dependencies.copy()

    def update(self, effect_fn: Callable, dependencies: List[Any]=None):
        """Updates the effect configuration"""
        self.effect_fn = effect_fn
        self.dependencies = dependencies

    def dispose(self):
        """Cleans up the effect"""
        if self._cleanup_fn:
            try:
                self._cleanup_fn()
            except Exception as e:
                self.logger.error(f'Cleanup error on dispose: {e}', exc_info=True)
        self._cleanup_fn = None
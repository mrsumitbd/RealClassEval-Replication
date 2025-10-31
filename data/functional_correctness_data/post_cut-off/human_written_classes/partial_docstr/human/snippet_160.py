from pruna.logging.filter import apply_warning_filter, remove_warning_filter
import logging
from typing import Any

class PrunaLoggerContext:
    """
    Context to manage the pruna_logger logging level and warning filters.

    Parameters
    ----------
    verbose : bool
        Whether to log at high detail or not.
    logging_level : int
        The logging level to set for the pruna_logger.
    """
    active_contexts: list['PrunaLoggerContext'] = []

    def __init__(self, verbose: bool, logging_level: int=logging.INFO) -> None:
        self.verbose = verbose
        self.original_level = 0
        self.logging_level = logging_level

    def __enter__(self) -> None:
        """Enter the context manager."""
        self.original_level = pruna_logger.getEffectiveLevel()
        self.active_contexts.append(self)
        if not self.verbose:
            apply_warning_filter()
        new_level = logging.DEBUG if self.verbose else self.logging_level
        if new_level > self.original_level or len(self.active_contexts) == 1:
            pruna_logger.setLevel(new_level)

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Exit the context manager.

        Parameters
        ----------
        exc_type : Any
            The type of the exception.
        exc_val : Any
            The value of the exception.
        exc_tb : Any
            The traceback of the exception.
        """
        pruna_logger.setLevel(self.original_level)
        if len(self.active_contexts) == 1:
            remove_warning_filter()
        self.active_contexts.remove(self)
from typing import Type, TYPE_CHECKING, Union, Tuple, Callable, Iterable, Mapping, Any, TypeVar
import multiprocessing.pool
import multiprocessing
import logging
import traceback

class ProcessLogger:
    """
    I am used by LoggingDaemonlessPool to get crash output out to the logger,
    instead of having process crashes be silent.
    """

    def __init__(self, callable: Callable) -> None:
        self.__callable = callable

    def __call__(self, *args, **kwargs) -> Any:
        try:
            return self.__callable(*args, **kwargs)
        except Exception:
            logger = multiprocessing.get_logger()
            if not logger.handlers:
                logger.addHandler(logging.StreamHandler())
            logger.error(traceback.format_exc())
            logger.handlers[0].flush()
            raise
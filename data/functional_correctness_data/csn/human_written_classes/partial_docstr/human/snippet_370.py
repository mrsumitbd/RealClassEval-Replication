from stravalib.protocol import RequestMethod
from collections.abc import Callable
from logging import Logger
import logging

class RateLimiter:

    def __init__(self) -> None:
        self.log: Logger = logging.getLogger(f'{self.__class__.__module__}.{self.__class__.__name__}')
        self.rules: list[Callable[[dict[str, str], RequestMethod], None]] = []

    def __call__(self, args: dict[str, str], method: RequestMethod) -> None:
        """Register another request is being issued."""
        for r in self.rules:
            r(args, method)
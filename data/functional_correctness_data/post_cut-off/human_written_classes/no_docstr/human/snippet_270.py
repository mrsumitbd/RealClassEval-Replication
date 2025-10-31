import logging
from loguru import logger

class DecoratorLoggerBase:

    def __init__(self, role: str, logger: logging.Logger=None, level=logging.DEBUG, rank: int=0, log_only_rank_0: bool=True):
        self.role = role
        self.logger = logger
        self.level = level
        self.rank = rank
        self.log_only_rank_0 = log_only_rank_0
        self.logging_function = self.log_by_logging
        if logger is None:
            self.logging_function = self.log_by_print

    def log_by_print(self, log_str):
        if not self.log_only_rank_0 or self.rank == 0:
            print(f'{self.role} {log_str}', flush=True)

    def log_by_logging(self, log_str):
        if self.logger is None:
            raise ValueError('Logger is not initialized')
        if not self.log_only_rank_0 or self.rank == 0:
            self.logger.log(self.level, f'{self.role} {log_str}')
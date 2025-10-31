import logging

class LogLevelFilter:

    def __init__(self, min_level=float('-inf'), max_level=float('inf')):
        self.min_level = min_level
        self.max_level = max_level

    def filter(self, record: logging.LogRecord):
        return self.min_level <= record.levelno <= self.max_level
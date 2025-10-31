from dragonlib.utils.logging_utils import setup_logging
from dragonpy.core.configs import machine_dict
import logging

class CliConfig:

    def __init__(self, machine, log, verbosity, log_formatter):
        self.machine = machine
        self.log = log
        self.verbosity = int(verbosity)
        self.log_formatter = log_formatter
        self.setup_logging()
        self.cfg_dict = {'verbosity': self.verbosity, 'trace': None}
        self.machine_run_func, self.machine_cfg = machine_dict[machine]

    def setup_logging(self):
        handler = logging.StreamHandler()
        setup_logging(level=self.verbosity, logger_name=None, handler=handler, log_formatter=self.log_formatter)
        if self.log is None:
            return
        for logger_cfg in self.log:
            logger_name, level = logger_cfg.rsplit(',', 1)
            level = int(level)
            setup_logging(level=level, logger_name=logger_name, handler=handler, log_formatter=self.log_formatter)
import logging
import os
import sys
import traceback

class Logger:
    """
    Redirects stdout to file (and console if needed)
    """

    def __init__(self, initial_message: str, log_path: str=None):
        self.debug = os.environ.get('LEMONADE_BUILD_DEBUG') == 'True'
        self.terminal = sys.stdout
        self.terminal_err = sys.stderr
        self.log_path = log_path
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f'{initial_message}\n')
        self.root_logger = logging.getLogger()
        self.handlers = [handler for handler in self.root_logger.handlers]
        for handler in self.handlers:
            self.root_logger.removeHandler(handler)
        if not self.debug:
            self.file_handler = logging.FileHandler(filename=log_path)
            self.file_handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.file_handler.setFormatter(formatter)
            self.root_logger.addHandler(self.file_handler)

    def __enter__(self):
        sys.stdout = self
        sys.stderr = self

    def __exit__(self, _exc_type, _exc_value, _exc_tb):
        if _exc_type:
            traceback.print_exception(_exc_type, _exc_value, _exc_tb)
        sys.stdout = self.terminal
        sys.stderr = self.terminal_err
        if not self.debug:
            self.file_handler.close()
            self.root_logger.removeHandler(self.file_handler)
            for handler in self.handlers:
                self.root_logger.addHandler(handler)

    def write(self, message):
        if self.log_path is not None:
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(message)
        if self.debug or self.log_path is None:
            self.terminal.write(message)
            self.terminal.flush()
            self.terminal_err.write(message)
            self.terminal_err.flush()

    def flush(self):
        pass
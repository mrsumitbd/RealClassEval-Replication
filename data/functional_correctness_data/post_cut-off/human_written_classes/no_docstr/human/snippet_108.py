import logging
from termcolor import colored
from datetime import datetime
import os

class MyLogger:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.propagate = False
        if os.getenv('TRITON_DIST_DEBUG', '').lower() in ('true', '1', 't'):
            self.logger.setLevel(logging.DEBUG)
            self.logger.debug('Debug logging enabled')

    def log(self, msg, level='info'):
        if level == 'info':
            self.logger.info(colored(f"> [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", 'cyan'))
        elif level == 'warning':
            self.logger.warning(colored(f"> [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", 'yellow'))
        elif level == 'error':
            self.logger.error(colored(f"> [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", 'red'))
        elif level == 'success':
            self.logger.info(colored(f"> [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", 'green'))
        elif level == 'debug':
            self.logger.debug(colored(f"> [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", 'magenta'))
        else:
            raise ValueError(colored(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Unknown log level: {level}", 'red'))
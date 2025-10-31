import logging
from os import path, getenv, makedirs, remove, rename, readlink, SEEK_END, SEEK_CUR, getpid, listdir, access, R_OK
from datetime import datetime

class PyRadioLog:
    PATTERN = '%(asctime)s - %(name)s:%(funcName)s():%(lineno)d - %(levelname)s: %(message)s'
    PATTERN_TITLE = '%(asctime)s | %(message)s'

    def __init__(self, pyradio_config):
        self.log_titles = False
        self.log_debug = False
        self.titles_handler = False
        self.debug_handler = None
        self._cnf = pyradio_config
        self._stations_dir = pyradio_config.stations_dir

    def configure_logger(self, recording_dir=None, debug=None, titles=None):
        logger = logging.getLogger('pyradio')
        logger.setLevel(logging.DEBUG)
        if debug or titles:
            if debug and (not self.log_debug):
                log_file = path.join(path.expanduser('~'), 'pyradio.log')
                self.debug_handler = logging.FileHandler(log_file)
                self.debug_handler.setLevel(logging.DEBUG)
                formatter = logging.Formatter(self.PATTERN)
                self.debug_handler.setFormatter(formatter)
                logger.addHandler(self.debug_handler)
                self.log_debug = True
            if titles and (not self.log_titles):
                if logger.isEnabledFor(logging.INFO):
                    logger.info('setting up pyradio-titles.log')
                if not path.exists(recording_dir):
                    try:
                        makedirs(recording_dir)
                    except:
                        pass
                if not path.exists(recording_dir):
                    self.log_titles = False
                    self.titles_handler = None
                    if logger.isEnabledFor(logging.ERROR):
                        logger.error(f'cannot start titles log on: "{recording_dir}"; directory does not exist')
                    return False
                else:
                    self.titles_handler = logging.handlers.RotatingFileHandler(path.join(recording_dir, 'pyradio-titles.log'), maxBytes=50000, backupCount=5)
                    self.titles_handler.setFormatter(logging.Formatter(fmt=self.PATTERN_TITLE, datefmt='%b %d (%a) %H:%M'))
                    self.titles_handler.setLevel(logging.CRITICAL)
                    logger.addHandler(self.titles_handler)
                    self.log_titles = True
                    logger.critical('=== Logging started')
                    if logger.isEnabledFor(logging.INFO):
                        logger.info(f'starting titles log on: "{recording_dir}"')
        if not titles and self.log_titles:
            if self.titles_handler:
                logger.critical('=== Logging stopped')
                logger.removeHandler(self.titles_handler)
                self.log_titles = False
                self.titles_handler = None
        logging.raiseExceptions = False
        logging.lastResort = None
        return True

    def _create_check_output_folder(self):
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        folder_name = f'{timestamp}-playlist-check'
        self._cnf.check_output_folder = path.join(self._cnf.state_dir, folder_name)
        try:
            if not path.exists(self._cnf.check_output_folder):
                makedirs(self._cnf.check_output_folder, exist_ok=True)
            if path.isdir(self._cnf.check_output_folder):
                return True
            else:
                return False
        except Exception:
            return False

    def tag_title(self, the_log):
        """ tags a title

            Returns:
                0: All ok
                1: Error
                2: Already tagged
        """
        if self._cnf.can_like_a_station():
            if logger.isEnabledFor(logging.CRITICAL):
                try:
                    the_log._write_title_to_log()
                except:
                    return 1
                return 0
        return 2
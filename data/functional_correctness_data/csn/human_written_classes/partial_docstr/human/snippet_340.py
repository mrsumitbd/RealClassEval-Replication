from shutil import copyfile
import logging
from copy import deepcopy
from os import path, remove
import json

class RadioBrowserConfig:
    """ RadioBrowser config calss

        Parameters:
            auto_save    : Boolean
            server       : string
            default      : int (id on terms)
            ping_timeout : int (ping timeout is seconds)
            ping_count   : int (number of ping packages)
            terms        : list of dicts (the actual search paremeters)
    """

    def __init__(self, stations_dir, data_dir):
        self.auto_save = False
        self.server = ''
        self.default = 1
        self.limit = '100'
        self.terms = []
        self.dirty = False
        self.ping_count = 1
        self.ping_timeout = 1
        self.config_file = path.join(stations_dir, 'radio-browser.conf')
        self.search_terms_file = path.join(data_dir, 'radio-browser-search-terms')

    def read_config(self):
        """ RadioBrowserConfig read config """
        for n in (self.config_file, self.search_terms_file):
            if path.exists(n + '.restore'):
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(f'restoring RadioBrowser config file: "{n}"')
                copyfile(n + '.restore', n)
                remove(n + '.restore')
        self.terms = [{'type': '', 'term': '100', 'post_data': {}}]
        self.default = 1
        self.auto_save = False
        self.limit = 100
        self.ping_count = 1
        self.ping_timeout = 1
        lines = []
        term_str = []
        try:
            with open(self.config_file, 'r', encoding='utf-8') as cfgfile:
                lines = [line.strip() for line in cfgfile if line.strip() and (not line.startswith('#'))]
        except (FileNotFoundError, IOError, UnicodeDecodeError):
            self.terms.append({'type': 'topvote', 'term': '100', 'post_data': {'reverse': 'true'}})
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('RadioBrowser: error reading config, reverting to defaults')
            return False
        for line in lines:
            if '=' in line:
                sp = line.split('=')
                for n in range(0, len(sp)):
                    sp[n] = sp[n].strip()
                if sp[1]:
                    if sp[0] == 'AUTO_SAVE_CONFIG':
                        self.auto_save = True if sp[1].lower() == 'true' else False
                    elif sp[0] == 'DEFAULT_SERVER':
                        self.server = sp[1]
                    elif sp[0] == 'DEFAULT_LIMIT':
                        try:
                            self.limit = int(sp[1])
                        except (IndexError, ValueError):
                            self.limit = '100'
                    elif sp[0] == 'SEARCH_TERM':
                        term_str.append(sp[1])
                    elif sp[0] == 'PING_COUNT':
                        try:
                            self.ping_count = int(sp[1])
                        except (IndexError, ValueError):
                            self.ping_count = 1
                    elif sp[0] == 'PING_TIMEOUT':
                        try:
                            self.ping_timeout = int(sp[1])
                        except (IndexError, ValueError):
                            self.ping_timeout = 1
        if path.exists(self.search_terms_file):
            try:
                with open(self.search_terms_file, 'r', encoding='utf-8') as searchfile:
                    lines = [line.strip() for line in searchfile if line.strip() and (not line.startswith('#'))]
                term_str = []
                for n in lines:
                    term_str.append(n)
            except (IOError, UnicodeDecodeError):
                pass
        if term_str:
            for n in range(0, len(term_str)):
                if term_str[n].startswith('*'):
                    term_str[n] = term_str[n][1:]
                    self.default = n + 1
                term_str[n] = term_str[n].replace("'", '"')
                try:
                    self.terms.append(json.loads(term_str[n]))
                except (json.JSONDecodeError, IndexError):
                    if logger.isEnabledFor(logging.ERROR):
                        logger.error(f'RadioBrowser: error inserting search term {n}')
                if 'limit' in self.terms[-1]['post_data'].keys():
                    if self.terms[-1]['post_data']['limit'] == str(self.limit):
                        self.terms[-1]['post_data'].pop('limit')
        else:
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('RadioBrowser: no search terms found, reverting to defaults')
            self.terms.append({'type': 'topvote', 'term': '100', 'post_data': {'reverse': 'true'}})
            return False
        self.terms[0]['term'] = self.limit
        return True

    def save_config(self, auto_save, search_history, search_default_history_index, default_server, default_ping_count, default_ping_timeout, default_max_number_of_results):
        if path.exists(self.config_file):
            copyfile(self.config_file, self.config_file + '.restore')
        self.auto_save = auto_save
        self.server = default_server if 'Random' not in default_server else ''
        self.default = default_max_number_of_results
        self.terms = deepcopy(search_history)
        txt = '################################################################\n#             RadioBrowser config file for PyRadio             #\n################################################################\n#\n# Auto save config\n# If True, the config will be automatically saved upon\n# closing RadioBrowser. Otherwise, confirmation will be asked\n# Possible values: True, False (default)\nAUTO_SAVE_CONFIG = '
        txt += str(auto_save)
        txt += '\n\n# Default server\n# The server that RadioBrowser will use by default\n# Default: empty string (use random server)\nDEFAULT_SERVER = '
        txt += default_server
        txt += '\n\n# Default maximum number of returned results\n# for any query to a RadioBrowser saerver\n# Default value: 100\nDEFAULT_LIMIT = '
        txt += str(default_max_number_of_results)
        txt += '\n\n# server pinging parameters\n# set any parameter to 0 to disable pinging\n# number of packages to send\nPING_COUNT = '
        txt += str(default_ping_count)
        txt += '\n# timeout in seconds\nPING_TIMEOUT = '
        txt += str(default_ping_timeout)
        try:
            with open(self.config_file, 'w', encoding='utf-8') as cfgfile:
                cfgfile.write(txt)
        except (IOError, OSError):
            if logger.isEnabledFor(logging.ERROR):
                logger.error('Saving Online Browser config file failed')
            return False
        if path.exists(self.config_file + '.restore'):
            remove(self.config_file + '.restore')
        self.dirty = False
        if path.exists(self.search_terms_file):
            copyfile(self.search_terms_file, self.search_terms_file + '.restore')
        try:
            with open(self.search_terms_file, 'w', encoding='utf-8') as cfgfile:
                for n in range(1, len(search_history)):
                    asterisk = '*' if n == search_default_history_index else ''
                    cfgfile.write(asterisk + str(search_history[n]) + '\n')
            if path.exists(self.search_terms_file + '.restore'):
                remove(self.search_terms_file + '.restore')
        except:
            if logger.isEnabledFor(logging.ERROR):
                logger.error('Saving Online Browser search terms file failed')
            return False
        if logger.isEnabledFor(logging.INFO):
            logger.info('Saved Online Browser config files')
        return True
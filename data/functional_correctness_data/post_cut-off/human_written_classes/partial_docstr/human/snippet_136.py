import os
from typing import Dict, List, Optional

class Stats:

    def __init__(self, cache_dir: str, build_name: str):
        self.file = stats_file(cache_dir, build_name)
        os.makedirs(os.path.dirname(self.file), exist_ok=True)
        if not os.path.exists(self.file):
            save_yaml({}, self.file)

    @property
    def stats(self):
        return _load_yaml(self.file)

    def _set_key(self, dict, keys: List['str'], value):
        """
        Recursive approach to safely setting a key within any level of hierarchy
        in a dictionary. If a parent key of the desired key does not exist, create
        it and set it with an empty dictionary before proceeding.

        The end result is: dict[keys[0]][keys[1]]...[keys[-1]] = value
        """
        if len(keys) == 1:
            dict[keys[0]] = value
        else:
            if keys[0] not in dict.keys():
                dict[keys[0]] = {}
            self._set_key(dict[keys[0]], keys[1:], value)

    def save_stat(self, key: str, value):
        """
        Save statistics to an yaml file in the build directory
        """
        stats_dict = self.stats
        self._set_key(stats_dict, [key], value)
        save_yaml(stats_dict, self.file)

    def save_sub_stat(self, parent_key: str, key: str, value):
        stats_dict = self.stats
        self._set_key(stats_dict, [parent_key, key], value)
        save_yaml(stats_dict, self.file)

    def save_eval_error_log(self, logfile_path):
        if logfile_path is None:
            return
        if os.path.exists(logfile_path):
            with open(logfile_path, 'r', encoding='utf-8') as f:
                full_log = f.readlines()
                start_cutoff = 5
                end_cutoff = -30
                max_full_length = start_cutoff + abs(end_cutoff)
                if len(full_log) > max_full_length:
                    log_start = _clean_logfile(full_log[:start_cutoff])
                    log_end = _clean_logfile(full_log[end_cutoff:])
                    truncation_notice = f'NOTICE: This copy of the log has been truncated to the first {start_cutoff} and last {abs(end_cutoff)} lines to save space. Please see {logfile_path} to see the full log.\n'
                    stats_log = log_start + truncation_notice + log_end
                else:
                    stats_log = _clean_logfile(full_log)
                self.save_stat(Keys.ERROR_LOG, stats_log)
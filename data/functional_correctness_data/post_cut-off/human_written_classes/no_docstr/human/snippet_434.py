import re
import logging
import sys
from dataclasses import dataclass
import os
from typing import Callable, Optional

@dataclass
class DebugFlags:
    log_level: int = logging.WARNING
    asserts: bool = False
    runtime_trace_dir: Optional[str] = None

    def set(self, part: str):
        m = re.match(SETTING_PART_PATTERN, part)
        if not m:
            logger.warning("Syntax error in %s flag: '%s'", FLAGS_ENV_NAME, part)
            return
        name = m.group(2)
        value = m.group(4)
        if value:
            logical_sense = value.upper() not in ['FALSE', 'OFF', '0']
        else:
            logical_sense = m.group(1) != '-'
        if name == 'log_level':
            if sys.version_info >= (3, 11):
                log_level_mapping = logging.getLevelNamesMapping()
                try:
                    self.log_level = log_level_mapping[value.upper()]
                except KeyError:
                    logger.warning("Log level '%s' unknown (ignored)", value)
            else:
                logger.warning("'log_level' flag requires Python >= 3.11")
        elif name == 'asserts':
            self.asserts = logical_sense
            global NDEBUG
            NDEBUG = not logical_sense
        elif name == 'runtime_trace_dir':
            self.runtime_trace_dir = value
        else:
            logger.warning("Unrecognized %s flag: '%s'", FLAGS_ENV_NAME, name)

    @staticmethod
    def parse(settings: str) -> 'DebugFlags':
        new_flags = DebugFlags()
        parts = settings.split(',')
        for part in parts:
            part = part.strip()
            if not part:
                continue
            new_flags.set(part)
        return new_flags

    @staticmethod
    def parse_from_env() -> 'DebugFlags':
        settings = os.getenv(FLAGS_ENV_NAME)
        if settings is None:
            new_flags = DebugFlags()
        else:
            new_flags = DebugFlags.parse(settings)
        for env_name, setting_name in ENV_SETTINGS_MAP.items():
            env_value = os.getenv(env_name)
            if env_value is not None:
                new_flags.set(f'{setting_name}={env_value}')
        logger.debug('Parsed debug flags from env %s: %r', FLAGS_ENV_NAME, new_flags)
        return new_flags
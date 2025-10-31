
import os
from typing import Dict
from dbt.exceptions import DbtInternalError
from dbt.events.types import InvalidStyleConfig
from dbt.events.functions import fire_event
from dbt.constants import JRDEV_DIR
from dbt_common.ui import PrintType, line_wrap_message
import yaml


class TerminalTextStyles:
    '''Manages loading, saving, and applying terminal text styles.'''

    def __init__(self, stylesheet_path: str = None):
        '''
        Initializes the style manager.
        Args:
            stylesheet_path: Optional path to the stylesheet. Defaults to
                             a file in the JRDEV_DIR.
        '''
        self.stylesheet_path = stylesheet_path or os.path.join(
            JRDEV_DIR, 'styles.yml')
        self.styles = self._get_default_styles()
        self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        '''Returns the default styles for each PrintType as a dictionary.'''
        return {pt.name: pt.value for pt in PrintType}

    def load_styles(self) -> None:
        '''Loads styles from the stylesheet file, merging them with defaults.'''
        try:
            with open(self.stylesheet_path, 'r') as f:
                text_styles = yaml.safe_load(f)
                if text_styles:
                    self.styles.update(text_styles)
        except FileNotFoundError:
            pass
        except yaml.YAMLError:
            fire_event(InvalidStyleConfig(path=self.stylesheet_path))
            # if the config is invalid, set it back to the defaults
            self.styles = self._get_default_styles()

    def save_styles(self) -> bool:
        '''Saves the current styles to the stylesheet file.'''
        try:
            with open(self.stylesheet_path, 'w') as f:
                yaml.dump(self.styles, f)
            return True
        except Exception:
            return False

    def get_style(self, print_type: PrintType) -> str:
        '''Gets the style string for a given PrintType.'''
        return self.styles.get(print_type.name, print_type.value)

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        '''Sets the style for a given PrintType.'''
        if not isinstance(print_type, PrintType):
            raise DbtInternalError(
                f'print_type must be PrintType, got {type(print_type)}')
        self.styles[print_type.name] = style_str
        self.save_styles()
        msg = line_wrap_message(
            f"Updated {print_type.name} to {style_str}\n"
            f"To persist these styles, re-run this command in a shell "
            f"that has `allow-unsafe-config` set to true."
        )
        fire_event(InvalidStyleConfig(path=msg))

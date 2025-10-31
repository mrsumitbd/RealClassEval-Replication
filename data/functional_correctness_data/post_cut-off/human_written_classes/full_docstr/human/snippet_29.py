from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple
import json

class LastUsedParams:
    """Manages last used parameters persistence (moved from last_used.py)."""

    def __init__(self, config_dir: Optional[Path]=None) -> None:
        """Initialize with config directory."""
        self.config_dir = config_dir or Path.home() / '.claude-monitor'
        self.params_file = self.config_dir / 'last_used.json'

    def save(self, settings: 'Settings') -> None:
        """Save current settings as last used."""
        try:
            params = {'theme': settings.theme, 'timezone': settings.timezone, 'time_format': settings.time_format, 'refresh_rate': settings.refresh_rate, 'reset_hour': settings.reset_hour, 'view': settings.view, 'timestamp': datetime.now().isoformat()}
            if settings.custom_limit_tokens:
                params['custom_limit_tokens'] = settings.custom_limit_tokens
            self.config_dir.mkdir(parents=True, exist_ok=True)
            temp_file = self.params_file.with_suffix('.tmp')
            with open(temp_file, 'w') as f:
                json.dump(params, f, indent=2)
            temp_file.replace(self.params_file)
            logger.debug(f'Saved last used params to {self.params_file}')
        except Exception as e:
            logger.warning(f'Failed to save last used params: {e}')

    def load(self) -> Dict[str, Any]:
        """Load last used parameters."""
        if not self.params_file.exists():
            return {}
        try:
            with open(self.params_file) as f:
                params = json.load(f)
            params.pop('timestamp', None)
            logger.debug(f'Loaded last used params from {self.params_file}')
            return params
        except Exception as e:
            logger.warning(f'Failed to load last used params: {e}')
            return {}

    def clear(self) -> None:
        """Clear last used parameters."""
        try:
            if self.params_file.exists():
                self.params_file.unlink()
                logger.debug('Cleared last used params')
        except Exception as e:
            logger.warning(f'Failed to clear last used params: {e}')

    def exists(self) -> bool:
        """Check if last used params exist."""
        return self.params_file.exists()
import json
from typing import Literal, Any, Optional, Iterator
import warnings

class SettingsOverrides:

    def __init__(self) -> None:
        object.__setattr__(self, '_overrides', {})

    def __setattr__(self, name: str, value: Any) -> None:
        if name == '_overrides':
            object.__setattr__(self, name, value)
            return
        warnings.warn("Setting values directly on agentic_doc.config.settings will be deprecated in a future release. Please, call parse(..., config=ParseConfig(api_key='xxx')) instead.", DeprecationWarning)
        self._overrides[name] = value

    def __getattr__(self, name: str) -> Any:
        if name in self._overrides:
            return self._overrides[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __iter__(self) -> Iterator[tuple[str, Any]]:
        return iter(self._overrides.items())

    def __str__(self) -> str:
        settings_dict = get_settings().model_dump()
        if 'vision_agent_api_key' in settings_dict:
            settings_dict['vision_agent_api_key'] = settings_dict['vision_agent_api_key'][:5] + '[REDACTED]'
        return f'{json.dumps(settings_dict, indent=2)}'
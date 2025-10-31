
from typing import Dict, KeysView, Any


class _CodeLanguageRegistry:
    '''Registry to store language configurations.'''

    def __init__(self) -> None:
        '''Initialize the registry.'''
        self._registry: Dict[str, Any] = {}

    def register(self, language: str, config: Any) -> None:
        '''Register a language configuration.'''
        self._registry[language] = config

    def get(self, language: str) -> Any:
        '''Get a language configuration.'''
        if language not in self._registry:
            raise KeyError(f"Language '{language}' is not registered.")
        return self._registry[language]

    def __contains__(self, language: str) -> bool:
        '''Check if a language is registered.'''
        return language in self._registry

    def __getitem__(self, language: str) -> Any:
        '''Get a language configuration.'''
        return self.get(language)

    def keys(self) -> KeysView[str]:
        '''Get all registered language keys.'''
        return self._registry.keys()

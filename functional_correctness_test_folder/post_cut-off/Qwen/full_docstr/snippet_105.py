
from typing import Dict, KeysView


class LanguageConfig:
    def __init__(self, **kwargs):
        self.config = kwargs


class _CodeLanguageRegistry:
    '''Registry to store language configurations.'''

    def __init__(self) -> None:
        '''Initialize the registry.'''
        self._registry: Dict[str, LanguageConfig] = {}

    def register(self, language: str, config: LanguageConfig) -> None:
        '''Register a language configuration.'''
        self._registry[language] = config

    def get(self, language: str) -> LanguageConfig:
        '''Get a language configuration.'''
        return self._registry.get(language)

    def __contains__(self, language: str) -> bool:
        '''Check if a language is registered.'''
        return language in self._registry

    def __getitem__(self, language: str) -> LanguageConfig:
        '''Get a language configuration.'''
        return self._registry[language]

    def keys(self) -> KeysView[str]:
        '''Get all registered language keys.'''
        return self._registry.keys()

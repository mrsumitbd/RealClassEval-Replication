from __future__ import annotations

from typing import Dict, KeysView


class _CodeLanguageRegistry:
    '''Registry to store language configurations.'''

    def __init__(self) -> None:
        '''Initialize the registry.'''
        self._registry: Dict[str, LanguageConfig] = {}

    def register(self, language: str, config: LanguageConfig) -> None:
        '''Register a language configuration.'''
        if not isinstance(language, str) or not language.strip():
            raise ValueError("language must be a non-empty string")
        if language in self._registry:
            raise ValueError(f"Language '{language}' is already registered")
        self._registry[language] = config

    def get(self, language: str) -> LanguageConfig:
        '''Get a language configuration.'''
        try:
            return self._registry[language]
        except KeyError as e:
            raise KeyError(f"Language '{language}' is not registered") from e

    def __contains__(self, language: str) -> bool:
        '''Check if a language is registered.'''
        return language in self._registry

    def __getitem__(self, language: str) -> LanguageConfig:
        '''Get a language configuration.'''
        return self.get(language)

    def keys(self) -> KeysView[str]:
        '''Get all registered language keys.'''
        return self._registry.keys()

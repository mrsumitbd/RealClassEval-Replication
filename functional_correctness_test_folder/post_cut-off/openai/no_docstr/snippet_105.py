
from typing import Dict, KeysView


class _CodeLanguageRegistry:
    """
    Registry for language configurations.
    """

    def __init__(self) -> None:
        self._registry: Dict[str, LanguageConfig] = {}

    def register(self, language: str, config: LanguageConfig) -> None:
        """
        Register a language configuration.
        """
        self._registry[language] = config

    def get(self, language: str) -> LanguageConfig:
        """
        Retrieve the configuration for a given language.
        Raises KeyError if the language is not registered.
        """
        return self._registry[language]

    def __contains__(self, language: str) -> bool:
        """
        Check if a language is registered.
        """
        return language in self._registry

    def __getitem__(self, language: str) -> LanguageConfig:
        """
        Allow dictionary-like access.
        """
        return self._registry[language]

    def keys(self) -> KeysView[str]:
        """
        Return a view of registered language keys.
        """
        return self._registry.keys()

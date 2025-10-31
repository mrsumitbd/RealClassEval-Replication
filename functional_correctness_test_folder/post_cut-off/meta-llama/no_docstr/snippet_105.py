
from typing import KeysView


class LanguageConfig:
    # Assuming LanguageConfig is defined elsewhere
    pass


class _CodeLanguageRegistry:

    def __init__(self) -> None:
        self._registry = {}

    def register(self, language: str, config: LanguageConfig) -> None:
        self._registry[language] = config

    def get(self, language: str) -> LanguageConfig:
        return self._registry.get(language)

    def __contains__(self, language: str) -> bool:
        return language in self._registry

    def __getitem__(self, language: str) -> LanguageConfig:
        return self._registry[language]

    def keys(self) -> KeysView[str]:
        return self._registry.keys()

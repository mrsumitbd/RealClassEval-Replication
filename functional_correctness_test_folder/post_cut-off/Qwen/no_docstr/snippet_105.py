
from typing import Dict, KeysView


class LanguageConfig:
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version


class _CodeLanguageRegistry:

    def __init__(self) -> None:
        self._registry: Dict[str, LanguageConfig] = {}

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

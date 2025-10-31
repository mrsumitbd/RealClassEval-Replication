from chonkie.types.code import LanguageConfig, MergeRule, SplitRule
from collections.abc import KeysView
from typing import Dict

class _CodeLanguageRegistry:
    """Registry to store language configurations."""

    def __init__(self) -> None:
        """Initialize the registry."""
        self.language_configs: Dict[str, LanguageConfig] = {}

    def register(self, language: str, config: LanguageConfig) -> None:
        """Register a language configuration."""
        self.language_configs[language] = config

    def get(self, language: str) -> LanguageConfig:
        """Get a language configuration."""
        return self.language_configs[language]

    def __contains__(self, language: str) -> bool:
        """Check if a language is registered."""
        return language in self.language_configs

    def __getitem__(self, language: str) -> LanguageConfig:
        """Get a language configuration."""
        return self.language_configs[language]

    def keys(self) -> KeysView[str]:
        """Get all registered language keys."""
        return self.language_configs.keys()
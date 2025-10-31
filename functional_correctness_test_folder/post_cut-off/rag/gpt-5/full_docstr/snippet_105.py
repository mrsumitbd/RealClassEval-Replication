from typing import Dict, KeysView


class _CodeLanguageRegistry:
    """Registry to store language configurations."""

    def __init__(self) -> None:
        """Initialize the registry."""
        self._configs: Dict[str, LanguageConfig] = {}

    def register(self, language: str, config: LanguageConfig) -> None:
        """Register a language configuration."""
        if not isinstance(language, str) or not language:
            raise ValueError("language must be a non-empty string")
        self._configs[language] = config

    def get(self, language: str) -> LanguageConfig:
        """Get a language configuration."""
        try:
            return self._configs[language]
        except KeyError:
            raise KeyError(f"Language not registered: {language}")

    def __contains__(self, language: str) -> bool:
        """Check if a language is registered."""
        return language in self._configs

    def __getitem__(self, language: str) -> LanguageConfig:
        """Get a language configuration."""
        return self.get(language)

    def keys(self) -> KeysView[str]:
        """Get all registered language keys."""
        return self._configs.keys()

class _CodeLanguageRegistry:
    '''Registry to store language configurations.'''

    def __init__(self) -> None:
        '''Initialize the registry.'''
        self._registry: dict[str, LanguageConfig] = {}

    def register(self, language: str, config: LanguageConfig) -> None:
        if not isinstance(language, str) or not language:
            raise ValueError("language must be a non-empty string")
        self._registry[language] = config

    def get(self, language: str) -> LanguageConfig:
        '''Get a language configuration.'''
        try:
            return self._registry[language]
        except KeyError as e:
            raise KeyError(f"Language not registered: {language}") from e

    def __contains__(self, language: str) -> bool:
        return language in self._registry

    def __getitem__(self, language: str) -> LanguageConfig:
        return self.get(language)

    def keys(self) -> KeysView[str]:
        return self._registry.keys()

from hdate.translations import TRANSLATIONS

class TranslatorMixin:
    """Translator Mixin class.

    Provides the capability of loading the correct string based on the language
    specified and the class name.
    """

    def __str__(self) -> str:
        if (name := getattr(self, 'name', None)):
            return self.get_translation(name)
        raise NameError(f'Unable to translate {self.__class__.__name__}. It is missing the name attribute')

    def available_languages(self) -> list[str]:
        """Return a list of available languages."""
        return list(TRANSLATIONS.keys())

    @property
    def translations(self) -> dict[str, str]:
        """Load the translations for the class."""
        lang = get_language()[:2]
        return TRANSLATIONS[lang].get(self.__class__.__name__, {})

    def get_translation(self, key: str) -> str:
        """Return the translation for the given key."""
        value = self.translations.get(key.lower(), None)
        if value is None:
            _LOGGER.error('Translation for %s not found', key)
            value = key
        return value
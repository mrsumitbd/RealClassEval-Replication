from typing import ClassVar

class LanguageMapping:
    """Value object for language-to-extension mappings.

    This encapsulates the domain knowledge of programming languages and their
    associated file extensions. It provides bidirectional mapping capabilities
    and is designed to be immutable and reusable across the application.
    """
    _LANGUAGE_TO_EXTENSIONS: ClassVar[dict[str, list[str]]] = {'python': ['py', 'pyw', 'pyx', 'pxd'], 'go': ['go'], 'javascript': ['js', 'jsx', 'mjs'], 'typescript': ['ts', 'tsx'], 'java': ['java'], 'csharp': ['cs'], 'cpp': ['cpp', 'cc', 'cxx', 'hpp'], 'c': ['c', 'h'], 'rust': ['rs'], 'php': ['php'], 'ruby': ['rb'], 'swift': ['swift'], 'kotlin': ['kt', 'kts'], 'scala': ['scala'], 'r': ['r', 'R'], 'matlab': ['m'], 'perl': ['pl', 'pm'], 'bash': ['sh', 'bash'], 'powershell': ['ps1'], 'sql': ['sql'], 'html': ['html', 'htm'], 'css': ['css', 'scss', 'sass'], 'yaml': ['yml', 'yaml'], 'json': ['json'], 'xml': ['xml'], 'markdown': ['md', 'markdown']}

    @classmethod
    def get_extensions_for_language(cls, language: str) -> list[str]:
        """Get file extensions for a given language.

        Args:
            language: The programming language name (case-insensitive)

        Returns:
            List of file extensions (without leading dots) for the language

        Raises:
            ValueError: If the language is not supported

        """
        language_lower = language.lower()
        extensions = cls._LANGUAGE_TO_EXTENSIONS.get(language_lower)
        if extensions is None:
            raise ValueError(f'Unsupported language: {language}')
        return extensions.copy()

    @classmethod
    def get_language_for_extension(cls, extension: str) -> str:
        """Get language for a given file extension.

        Args:
            extension: The file extension (with or without leading dot)

        Returns:
            The programming language name

        Raises:
            ValueError: If the extension is not supported

        """
        ext_clean = extension.removeprefix('.').lower()
        for language, extensions in cls._LANGUAGE_TO_EXTENSIONS.items():
            if ext_clean in extensions:
                return language
        raise ValueError(f'Unsupported file extension: {extension}')

    @classmethod
    def get_extension_to_language_map(cls) -> dict[str, str]:
        """Get a mapping from file extensions to language names.

        Returns:
            Dictionary mapping file extensions (without leading dots) to language names

        """
        extension_map = {}
        for language, extensions in cls._LANGUAGE_TO_EXTENSIONS.items():
            for extension in extensions:
                extension_map[extension] = language
        return extension_map

    @classmethod
    def get_supported_languages(cls) -> list[str]:
        """Get list of all supported programming languages.

        Returns:
            List of supported language names

        """
        return list(cls._LANGUAGE_TO_EXTENSIONS.keys())

    @classmethod
    def get_supported_extensions(cls) -> list[str]:
        """Get list of all supported file extensions.

        Returns:
            List of supported file extensions (without leading dots)

        """
        extensions = []
        for ext_list in cls._LANGUAGE_TO_EXTENSIONS.values():
            extensions.extend(ext_list)
        return extensions

    @classmethod
    def is_supported_language(cls, language: str) -> bool:
        """Check if a language is supported.

        Args:
            language: The programming language name (case-insensitive)

        Returns:
            True if the language is supported, False otherwise

        """
        return language.lower() in cls._LANGUAGE_TO_EXTENSIONS

    @classmethod
    def is_supported_extension(cls, extension: str) -> bool:
        """Check if a file extension is supported.

        Args:
            extension: The file extension (with or without leading dot)

        Returns:
            True if the extension is supported, False otherwise

        """
        try:
            cls.get_language_for_extension(extension)
        except ValueError:
            return False
        return True

    @classmethod
    def get_extensions_with_fallback(cls, language: str) -> list[str]:
        """Get file extensions for a language, falling back to passed language name.

        Args:
            language: The programming language name (case-insensitive)

        Returns:
            List of file extensions (without leading dots) for the language, or
            [language.lower()] if not found.

        """
        language_lower = language.lower()
        if cls.is_supported_language(language_lower):
            return cls.get_extensions_for_language(language_lower)
        return [language_lower]
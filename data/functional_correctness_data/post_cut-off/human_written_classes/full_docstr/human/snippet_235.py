from dataclasses import dataclass

@dataclass(frozen=True)
class LanguageExtensions:
    """Value object for language to file extension mappings."""
    language: str
    extensions: list[str]

    @classmethod
    def get_supported_languages(cls) -> list[str]:
        """Get all supported programming languages."""
        return ['python', 'javascript', 'typescript', 'java', 'c', 'cpp', 'csharp', 'go', 'rust', 'php', 'ruby', 'swift', 'kotlin', 'scala', 'r', 'sql', 'html', 'css', 'json', 'yaml', 'xml', 'markdown', 'shell']

    @classmethod
    def get_extensions_for_language(cls, language: str) -> list[str]:
        """Get file extensions for a given language."""
        language_map = {'python': ['.py', '.pyw', '.pyi'], 'javascript': ['.js', '.jsx', '.mjs'], 'typescript': ['.ts', '.tsx'], 'java': ['.java'], 'c': ['.c', '.h'], 'cpp': ['.cpp', '.cc', '.cxx', '.hpp', '.hxx'], 'csharp': ['.cs'], 'go': ['.go'], 'rust': ['.rs'], 'php': ['.php'], 'ruby': ['.rb'], 'swift': ['.swift'], 'kotlin': ['.kt', '.kts'], 'scala': ['.scala', '.sc'], 'r': ['.r', '.R'], 'sql': ['.sql'], 'html': ['.html', '.htm'], 'css': ['.css', '.scss', '.sass', '.less'], 'json': ['.json'], 'yaml': ['.yaml', '.yml'], 'xml': ['.xml'], 'markdown': ['.md', '.markdown'], 'shell': ['.sh', '.bash', '.zsh', '.fish']}
        return language_map.get(language.lower(), [])

    @classmethod
    def is_supported_language(cls, language: str) -> bool:
        """Check if a language is supported."""
        return language.lower() in cls.get_supported_languages()

    @classmethod
    def get_extensions_or_fallback(cls, language: str) -> list[str]:
        """Get extensions for language or return language as extension if not found."""
        language_lower = language.lower()
        if cls.is_supported_language(language_lower):
            return cls.get_extensions_for_language(language_lower)
        return [language_lower]
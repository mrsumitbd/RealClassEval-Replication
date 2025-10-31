import re

class ShellUtils:
    """Utilities for processing shell commands within Makefile recipes."""
    START_KEYWORDS = ('if', 'for', 'while', 'case', 'until')
    CONTINUATION_KEYWORDS = ('elif', 'else')
    END_KEYWORDS = ('fi', 'done', 'esac')
    END_KEYWORDS_WITH_SEMICOLON = ('fi;', 'done;', 'esac;')
    ALL_KEYWORDS = START_KEYWORDS + CONTINUATION_KEYWORDS + END_KEYWORDS + END_KEYWORDS_WITH_SEMICOLON
    SIMPLE_KEYWORDS = START_KEYWORDS + CONTINUATION_KEYWORDS + ('do', 'then')
    OPERATORS = ('&&', '||', ';', '|', '>', '<', '>>', '<<', '$(', '`')

    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        """Check if a line starts a shell control structure."""
        stripped = line.lstrip('@-+ ')
        control_patterns = ['^if\\s+\\[', '^for\\s+', '^while\\s+', '^case\\s+', '^until\\s+', '^{\\s*$']
        return any((re.match(pattern, stripped) for pattern in control_patterns))

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        """Check if a line ends a shell control structure."""
        stripped = line.lstrip('@-+ \t').rstrip()
        return any((stripped.startswith(kw) for kw in ShellUtils.END_KEYWORDS)) or any((stripped.endswith(kw) for kw in ShellUtils.END_KEYWORDS_WITH_SEMICOLON))

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        """Check if content contains shell operators that suggest deliberate structure."""
        return any((op in line for op in ShellUtils.OPERATORS))
import re


class ShellUtils:
    '''Utilities for processing shell commands within Makefile recipes.'''

    _SHELL_CONTROL_START_PATTERNS = [
        r'^\s*if\b',
        r'^\s*for\b',
        r'^\s*while\b',
        r'^\s*case\b',
        r'^\s*until\b',
        r'^\s*select\b',
        r'^\s*do\b',
        r'^\s*then\b',
        r'^\s*else\b',
        r'^\s*elif\b',
        r'^\s*function\b',
        r'^\s*\{',
    ]
    _SHELL_CONTROL_END_PATTERNS = [
        r'^\s*fi\b',
        r'^\s*done\b',
        r'^\s*esac\b',
        r'^\s*\}',
    ]
    _SHELL_OPERATORS = [
        '&&', '||', ';', '|', '>', '>>', '<', '2>', '2>>', '&>', '&>>', '>&', '<<', '<<<', '||', '&&', ';;'
    ]

    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        '''Check if a line starts a shell control structure.'''
        for pat in ShellUtils._SHELL_CONTROL_START_PATTERNS:
            if re.match(pat, line):
                return True
        return False

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        '''Check if a line ends a shell control structure.'''
        for pat in ShellUtils._SHELL_CONTROL_END_PATTERNS:
            if re.match(pat, line):
                return True
        return False

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        '''Check if content contains shell operators that suggest deliberate structure.'''
        # Remove quoted strings to avoid false positives
        def _remove_quoted(s):
            return re.sub(r'''(['"]).*?\1''', '', s)
        s = _remove_quoted(line)
        for op in ShellUtils._SHELL_OPERATORS:
            # Use word boundaries for operators that are words
            if op in {'&&', '||', ';;'}:
                if re.search(r'(?<!\w)'+re.escape(op)+r'(?!\w)', s):
                    return True
            else:
                if op in s:
                    return True
        return False

class ShellUtils:
    '''Utilities for processing shell commands within Makefile recipes.'''

    @staticmethod
    def _normalize(line: str) -> str:
        if line is None:
            return ""
        s = line.strip()
        # Remove common Make recipe prefixes
        while s.startswith(('@', '-', '+')):
            s = s[1:].lstrip()
        return s

    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        '''Check if a line starts a shell control structure.'''
        import re
        s = ShellUtils._normalize(line)

        if not s:
            return False

        # Direct openers
        if re.match(r'^(if|for|while|until|case|select)\b', s):
            return True

        # Function definition openers
        if re.match(r'^[A-Za-z_][A-Za-z0-9_]*\s*\(\s*\)\s*\{', s):
            return True

        # Bare block openers
        if re.match(r'^\{(\s|$)', s):
            return True

        # Subshell openers
        if re.match(r'^\((\s|$)', s):
            return True

        return False

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        '''Check if a line ends a shell control structure.'''
        import re
        s = ShellUtils._normalize(line)

        if not s:
            return False

        # Direct closers
        if re.match(r'^(fi|done|esac)\b', s):
            return True

        # Bare block/subshell closers
        if re.match(r'^\}', s) or re.match(r'^\)', s):
            return True

        return False

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        '''Check if content contains shell operators that suggest deliberate structure.'''
        if not line:
            return False

        s = ShellUtils._normalize(line)

        # Quick checks for common operators
        operators = [
            '&&', '||', '||', ';;', '|', ';',
            '>>', '<<', '<<<', '>&', '2>&1',
            '1>', '2>', '>|', '>', '<',
            '$(', '`', '&'
        ]

        for op in operators:
            if op in s:
                return True

        return False

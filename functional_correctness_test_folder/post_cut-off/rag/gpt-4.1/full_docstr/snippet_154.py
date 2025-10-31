import re


class ShellUtils:
    '''Utilities for processing shell commands within Makefile recipes.'''

    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        '''Check if a line starts a shell control structure.'''
        # Common shell control starts: if, for, while, until, case, select, function definitions
        line_strip = line.lstrip()
        patterns = [
            r'^(if|for|while|until|case|select)\b',  # control keywords
            # function definition: foo() {
            r'^[a-zA-Z_][a-zA-Z0-9_]*\s*\(\)\s*\{',
            r'^\{',  # block start
        ]
        for pat in patterns:
            if re.match(pat, line_strip):
                return True
        return False

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        '''Check if a line ends a shell control structure.'''
        # Common shell control ends: fi, done, esac, }, elif, else
        line_strip = line.lstrip()
        patterns = [
            r'^(fi|done|esac|elif|else)\b',
            r'^\}',  # block end
        ]
        for pat in patterns:
            if re.match(pat, line_strip):
                return True
        return False

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        '''Check if content contains shell operators that suggest deliberate structure.'''
        # Look for &&, ||, |, ;, ``, $(), >, <, >>, <<, &, ||, &&
        # Exclude inside quotes for basic cases
        # This is a heuristic, not a full shell parser
        # Remove quoted substrings
        def remove_quoted(s):
            return re.sub(r'(["\']).*?\1', '', s)
        s = remove_quoted(line)
        operators = [
            r'\&\&', r'\|\|', r'\|', r';', r'`', r'\$\(', r'>', r'<', r'>>', r'<<', r'\&'
        ]
        for op in operators:
            if re.search(op, s):
                return True
        return False

import re


class ShellUtils:
    '''Utilities for processing shell commands within Makefile recipes.'''

    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        '''Check if a line starts a shell control structure.'''
        line = line.strip()
        # Common shell control starts: if, for, while, until, case, select, function
        control_start_patterns = [
            # e.g. if, for, while, until, case, select
            r'^(if|for|while|until|case|select)\b',
            # function definition: foo() {
            r'^\w+\s*\(\)\s*\{',
            r'^\{',                                 # block start: {
        ]
        for pat in control_start_patterns:
            if re.match(pat, line):
                return True
        # Also: do at end of line (for/while/until loops)
        if re.match(r'.*\bdo\s*;?\s*$', line):
            return True
        return False

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        '''Check if a line ends a shell control structure.'''
        line = line.strip()
        # Common shell control ends: fi, done, esac, }, elif, else
        control_end_patterns = [
            r'^(fi|done|esac|elif|else)\b',
            r'^\}',
        ]
        for pat in control_end_patterns:
            if re.match(pat, line):
                return True
        return False

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        '''Check if content contains shell operators that suggest deliberate structure.'''
        # Look for &&, ||, |, ;, ``, $(), >, <, >>, <<, &, ||, &&, ( )
        # Exclude ; at end of line only (as it may be a line terminator)
        operators = [
            r'\&\&', r'\|\|', r'\|', r';', r'`', r'\$\(', r'>', r'<', r'>>', r'<<', r'\(', r'\)', r'\&'
        ]
        for op in operators:
            if re.search(op, line):
                return True
        return False

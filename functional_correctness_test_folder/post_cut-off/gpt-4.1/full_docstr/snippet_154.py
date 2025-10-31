
import re


class ShellUtils:
    '''Utilities for processing shell commands within Makefile recipes.'''

    # Shell control structure starters and enders
    _control_start_keywords = [
        'if', 'for', 'while', 'until', 'case', 'select'
    ]
    _control_end_keywords = [
        'fi', 'done', 'esac'
    ]

    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        '''Check if a line starts a shell control structure.'''
        line = line.strip()
        # Match: if ..., for ..., while ..., until ..., case ..., select ...
        for kw in ShellUtils._control_start_keywords:
            # e.g., "if [ ... ];" or "if [ ... ]" or "if test ...", etc.
            if re.match(rf'^{kw}\b', line):
                return True
        return False

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        '''Check if a line ends a shell control structure.'''
        line = line.strip()
        # Match: fi, done, esac (possibly with trailing ';' or '&&' or '||')
        for kw in ShellUtils._control_end_keywords:
            if re.match(rf'^{kw}\b', line):
                return True
        return False

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        '''Check if content contains shell operators that suggest deliberate structure.'''
        # Common shell operators: &&, ||, |, ;, ``, $(), >, >>, <, <<, &, ()
        # We'll look for &&, ||, |, ;, >, >>, <, <<, &, ( )
        # Avoid matching inside quotes (simple heuristic)
        # Remove quoted substrings
        def remove_quoted(s):
            return re.sub(r'(["\']).*?\1', '', s)
        s = remove_quoted(line)
        # Look for operators
        operators = [
            r'&&', r'\|\|', r'\|', r';', r'>>', r'<<', r'>', r'<', r'&', r'\(', r'\)'
        ]
        pattern = '|'.join(operators)
        return re.search(pattern, s) is not None

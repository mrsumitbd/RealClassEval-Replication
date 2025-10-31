
import re


class ShellUtils:
    '''Utilities for processing shell commands within Makefile recipes.'''

    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        '''Check if a line starts a shell control structure.'''
        line = line.strip()
        return bool(re.match(r'^(if|for|while|case|function|\(|{|then|do)\b', line))

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        '''Check if a line ends a shell control structure.'''
        line = line.strip()
        return bool(re.match(r'^(fi|done|esac|\)|}|else|elif)\b', line))

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        '''Check if content contains shell operators that suggest deliberate structure.'''
        line = line.strip()
        return bool(re.search(r'[;|&]', line))

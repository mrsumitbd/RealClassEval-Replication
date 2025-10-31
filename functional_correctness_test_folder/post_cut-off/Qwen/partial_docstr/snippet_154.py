
class ShellUtils:
    '''Utilities for processing shell commands within Makefile recipes.'''
    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        return line.strip().startswith(('if', 'ifdef', 'ifndef', 'else', 'elif', 'for'))

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        '''Check if a line ends a shell control structure.'''
        return line.strip().startswith(('endif', 'endfor'))

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        '''Check if content contains shell operators that suggest deliberate structure.'''
        operators = {'&&', '||', ';', '&&&', '|||', '&',
                     '|', '(', ')', '${', '}', '`', '$(', ')'}
        return any(op in line for op in operators)

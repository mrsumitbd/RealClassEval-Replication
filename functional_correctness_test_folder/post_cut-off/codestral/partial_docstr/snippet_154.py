
class ShellUtils:
    '''Utilities for processing shell commands within Makefile recipes.'''
    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        line = line.strip()
        return line.startswith('if ') or line.startswith('for ') or line.startswith('while ') or line.startswith('case ')

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        '''Check if a line ends a shell control structure.'''
        line = line.strip()
        return line == 'fi' or line == 'done' or line == 'esac'

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        '''Check if content contains shell operators that suggest deliberate structure.'''
        operators = ['&&', '||', ';', '|', '(', ')']
        for op in operators:
            if op in line:
                return True
        return False

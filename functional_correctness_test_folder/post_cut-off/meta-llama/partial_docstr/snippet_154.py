
class ShellUtils:
    '''Utilities for processing shell commands within Makefile recipes.'''
    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        line = line.strip()
        return line.endswith('{') or line.endswith('(') or line.endswith('do') or line.endswith(';') or line.endswith('\\')

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        '''Check if a line ends a shell control structure.'''
        line = line.strip()
        return line.startswith('}') or line.startswith(')') or line == 'done'

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        '''Check if content contains shell operators that suggest deliberate structure.'''
        line = line.strip()
        shell_operators = ['&&', '||', '|', ';', '&&', '||', ';;', 'do', 'done',
                           'if', 'then', 'else', 'fi', 'for', 'while', 'until', 'case', 'esac']
        for operator in shell_operators:
            if operator in line:
                return True
        return False

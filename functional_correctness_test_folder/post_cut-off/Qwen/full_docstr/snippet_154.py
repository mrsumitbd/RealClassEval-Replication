
class ShellUtils:
    '''Utilities for processing shell commands within Makefile recipes.'''
    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        '''Check if a line starts a shell control structure.'''
        return line.strip().startswith(('if', 'for', 'while', 'case', 'select', 'until'))

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        '''Check if a line ends a shell control structure.'''
        return line.strip() in ('fi', 'done', 'esac', ';;')

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        '''Check if content contains shell operators that suggest deliberate structure.'''
        operators = ('&&', '||', ';', '&&&', '|||', '&', '|',
                     '(', ')', '<<', '>>', '<<-', '>>-', '<', '>', '<<<')
        return any(op in line for op in operators)

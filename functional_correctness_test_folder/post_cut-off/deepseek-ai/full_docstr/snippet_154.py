
class ShellUtils:
    '''Utilities for processing shell commands within Makefile recipes.'''
    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        '''Check if a line starts a shell control structure.'''
        stripped = line.strip()
        return stripped.startswith(('if ', 'for ', 'while ', 'case ', 'select ')) or \
            stripped.startswith(('if[', 'for[', 'while[', 'case[', 'select[')) or \
            stripped.startswith(('{', '(', '[[', '[['))

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        '''Check if a line ends a shell control structure.'''
        stripped = line.strip()
        return stripped in ('fi', 'done', 'esac', '}', ')', ']]', ']')

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        '''Check if content contains shell operators that suggest deliberate structure.'''
        operators = {'&&', '||', ';', '|', '&', '>', '<', '>>',
                     '<<', '<<<', '>|', '<>', '2>', '2>>', '&>', '&>>'}
        return any(op in line for op in operators)

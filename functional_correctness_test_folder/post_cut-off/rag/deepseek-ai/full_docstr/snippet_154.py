
class ShellUtils:
    '''Utilities for processing shell commands within Makefile recipes.'''
    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        '''Check if a line starts a shell control structure.'''
        stripped_line = line.strip()
        return stripped_line.startswith(('if ', 'for ', 'while ', 'case ', 'select ')) or stripped_line.startswith(('{', 'then', 'do'))

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        '''Check if a line ends a shell control structure.'''
        stripped_line = line.strip()
        return stripped_line in ('fi', 'done', 'esac', '}')

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        '''Check if content contains shell operators that suggest deliberate structure.'''
        operators = {'&&', '||', ';', '|', '&', '>',
                     '<', '>>', '<<', '2>', '2>>', '1>', '1>>'}
        return any(op in line for op in operators)

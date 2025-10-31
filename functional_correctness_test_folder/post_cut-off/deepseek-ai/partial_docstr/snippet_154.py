
class ShellUtils:
    '''Utilities for processing shell commands within Makefile recipes.'''
    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        stripped = line.strip()
        return stripped.startswith(('if ', 'for ', 'while ', 'case ')) or stripped in ('if', 'for', 'while', 'case')

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        '''Check if a line ends a shell control structure.'''
        stripped = line.strip()
        return stripped == 'fi' or stripped == 'done' or stripped == 'esac' or stripped.endswith('; fi') or stripped.endswith('; done') or stripped.endswith('; esac')

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        '''Check if content contains shell operators that suggest deliberate structure.'''
        operators = {'&&', '||', ';', '|', '&', '>',
                     '<', '>>', '<<', '2>', '2>>', '1>', '1>>'}
        return any(op in line for op in operators)


class ShellUtils:
    '''Utilities for processing shell commands within Makefile recipes.'''
    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        line = line.strip()
        # Check for common shell control structure starts
        control_starts = [
            'if ', 'for ', 'while ', 'case ', 'until ', 'select ',
            'do', 'then', '{', '('
        ]
        # Check for lines ending with 'do' or 'then'
        if line.endswith('do') or line.endswith('then'):
            return True
        # Check for lines starting with control keywords
        for kw in control_starts:
            if line.startswith(kw):
                return True
        return False

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        '''Check if a line ends a shell control structure.'''
        line = line.strip()
        # Common shell control structure ends
        control_ends = ['fi', 'done', 'esac', '}', ')']
        return line in control_ends

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        '''Check if content contains shell operators that suggest deliberate structure.'''
        # Common shell operators
        operators = ['&&', '||', ';', '|', '>', '<', '>>', '2>', '&>', '>&']
        for op in operators:
            if op in line:
                return True
        return False

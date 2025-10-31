
class ShellUtils:

    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        """Check if a line starts with a shell control structure."""
        line = line.strip()
        control_structures = ['if', 'for', 'while', 'until', 'case']
        for structure in control_structures:
            if line.startswith(structure):
                return True
        return False

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        """Check if a line contains the end of a shell control structure."""
        line = line.strip()
        if line == 'fi' or line == 'done' or line.startswith('esac'):
            return True
        return False

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        """Check if a line contains shell operators."""
        shell_operators = ['&&', '||', ';', '|', '&', '>', '>>', '<', '<<']
        for operator in shell_operators:
            if operator in line:
                return True
        return False

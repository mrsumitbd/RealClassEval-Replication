
class ShellUtils:
    """Utilities for processing shell commands within Makefile recipes."""

    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        """Check if a line starts a shell control structure."""
        line = line.strip()
        return line.startswith(('if', 'for', 'while', 'until', 'case'))

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        """Check if a line ends a shell control structure."""
        line = line.strip()
        return line.endswith((';;', 'fi', 'done'))

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        """Check if content contains shell operators that suggest deliberate structure."""
        line = line.strip()
        shell_operators = ['&&', '||', ';', '|', '&&', '||']
        for operator in shell_operators:
            if operator in line:
                return True
        return False


class ShellUtils:

    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        stripped = line.strip()
        # Common shell control start keywords
        control_starts = ('if ', 'for ', 'while ',
                          'case ', 'until ', 'select ')
        return any(stripped.startswith(kw) for kw in control_starts)

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        stripped = line.strip()
        # Common shell control end keywords
        control_ends = ('fi', 'done', 'esac')
        return stripped in control_ends

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        # Common shell operators
        operators = ['&&', '||', '|', ';', '>', '>>', '<', '2>', '&']
        return any(op in line for op in operators)


class ShellUtils:

    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        control_keywords = ['if', 'for', 'while', 'until', 'case']
        stripped_line = line.strip()
        for keyword in control_keywords:
            if stripped_line.startswith(f'{keyword} ') or stripped_line.startswith(f'{keyword}('):
                return True
        return False

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        stripped_line = line.strip()
        return stripped_line == 'fi' or stripped_line == 'done' or stripped_line == 'esac'

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        operators = ['&&', '||', ';', '|', '&',
                     '>', '<', '>>', '<<', '2>', '2>>', '&>']
        for op in operators:
            if op in line:
                return True
        return False

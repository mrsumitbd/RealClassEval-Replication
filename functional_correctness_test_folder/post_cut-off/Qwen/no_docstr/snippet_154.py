
class ShellUtils:

    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        return line.strip().startswith(('if', 'for', 'while', 'case', 'select', 'until', 'function'))

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        return line.strip().endswith(('fi', 'done', 'esac', ';;', '}')

    @ staticmethod
    def contains_shell_operators(line: str) -> bool:
        operators=['&&', '||', ';;', '|', '&', ';',
            '(', ')', '<', '>', '<<', '>>', '<<<', '>&', '<&', '>>>', '<<-', '<>', '!', '{', '}']
        return any(op in line for op in operators)

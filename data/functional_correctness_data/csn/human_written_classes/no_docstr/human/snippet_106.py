class Format:

    @staticmethod
    def parsable(problem, filename):
        return f'{filename}:{problem.line}:{problem.column}: [{problem.level}] {problem.message}'

    @staticmethod
    def standard(problem, filename):
        line = f'  {problem.line}:{problem.column}'
        line += max(12 - len(line), 0) * ' '
        line += problem.level
        line += max(21 - len(line), 0) * ' '
        line += problem.desc
        if problem.rule:
            line += f'  ({problem.rule})'
        return line

    @staticmethod
    def standard_color(problem, filename):
        line = f'  \x1b[2m{problem.line}:{problem.column}\x1b[0m'
        line += max(20 - len(line), 0) * ' '
        if problem.level == 'warning':
            line += f'\x1b[33m{problem.level}\x1b[0m'
        else:
            line += f'\x1b[31m{problem.level}\x1b[0m'
        line += max(38 - len(line), 0) * ' '
        line += problem.desc
        if problem.rule:
            line += f'  \x1b[2m({problem.rule})\x1b[0m'
        return line

    @staticmethod
    def github(problem, filename):
        line = f'::{problem.level} file={filename},line={problem.line},col={problem.column}::{problem.line}:{problem.column} '
        if problem.rule:
            line += f'[{problem.rule}] '
        line += problem.desc
        return line
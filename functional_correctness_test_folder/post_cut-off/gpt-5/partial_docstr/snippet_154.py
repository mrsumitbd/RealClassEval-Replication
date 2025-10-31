class ShellUtils:
    '''Utilities for processing shell commands within Makefile recipes.'''

    @staticmethod
    def _strip_recipe_prefix(line: str) -> str:
        if line is None:
            return ''
        s = line.lstrip()
        # Make recipe prefixes commonly include @, -, + possibly repeated
        i = 0
        while i < len(s) and s[i] in '@-+':
            i += 1
        return s[i:].strip()

    @staticmethod
    def _is_comment_or_empty(line: str) -> bool:
        if not line:
            return True
        s = line.strip()
        return s == '' or s.startswith('#')

    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        s = ShellUtils._strip_recipe_prefix(line)
        if ShellUtils._is_comment_or_empty(s):
            return False

        ls = s.strip()

        # Function definition or group/subshell start
        if ls.endswith('{') or ls.endswith('('):
            return True

        # case ... in
        if ls.startswith('case ') and ls.endswith(' in'):
            return True

        # if/while/until/for/select with then/do
        tokens = ls.split()
        if not tokens:
            return False

        first = tokens[0]
        if first in ('if', 'while', 'until'):
            # Often ends with 'then'
            if ls.endswith(' then') or ls.endswith('then'):
                return True
            # Even if 'then' is on next line, it's still a start of control structure
            return True

        if first in ('for', 'select'):
            # Typically ends with 'do'
            if ls.endswith(' do') or ls.endswith('do'):
                return True
            # Consider it start anyway
            return True

        # else/elif are also control-structure boundaries that "start" a block
        if first in ('else', 'elif'):
            return True

        # do after for/while/until on previous lines
        if ls == 'do' or ls.endswith(' do'):
            return True

        # Explicit 'then' line
        if ls == 'then' or ls.endswith(' then'):
            return True

        return False

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        '''Check if a line ends a shell control structure.'''
        s = ShellUtils._strip_recipe_prefix(line)
        if ShellUtils._is_comment_or_empty(s):
            return False

        ls = s.strip().rstrip(';').strip()

        # Simple terminators
        if ls in ('fi', 'done', 'esac'):
            return True

        # Block/group end
        if ls.endswith(')'):
            # Avoid common command uses like subshell end are still control end
            return True
        if ls.endswith('}'):
            return True

        return False

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        '''Check if content contains shell operators that suggest deliberate structure.'''
        s = ShellUtils._strip_recipe_prefix(line)
        if ShellUtils._is_comment_or_empty(s):
            return False

        # Common shell operators and control keywords
        operators = [
            '&&', '||', ';;', '|', ';', '&',
            '>>', '<<', '<<<', '>|', '2>&1', '>&', '1>', '2>', '>', '<',
            '$(', '`', '${', '$((',
        ]
        keywords = [
            'if ', 'then', 'else', 'elif', 'fi',
            'for ', 'select ', 'while ', 'until ', 'do', 'done',
            'case ', ' in', 'esac',
        ]

        ls = s

        for op in operators:
            if op in ls:
                return True
        for kw in keywords:
            if kw in ls:
                return True

        # Braces and parentheses can also indicate grouping/subshell/function
        stripped = ls.strip()
        if any(ch in stripped for ch in '{}()'):
            return True

        return False

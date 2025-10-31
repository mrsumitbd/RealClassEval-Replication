class ShellUtils:

    @staticmethod
    def _strip_comments(line: str) -> str:
        s = line
        in_s = False
        in_d = False
        esc = False
        for i, ch in enumerate(s):
            if esc:
                esc = False
                continue
            if ch == '\\':
                esc = True
                continue
            if not in_d and ch == "'" and not in_s:
                in_s = True
                continue
            elif in_s:
                if ch == "'":
                    in_s = False
                continue
            if not in_s and ch == '"' and not in_d:
                in_d = True
                continue
            elif in_d:
                if ch == '"' and not esc:
                    in_d = False
                continue
            if ch == '#' and not in_s and not in_d:
                return s[:i]
        return s

    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        import re
        l = ShellUtils._strip_comments(line or "").strip()
        if not l:
            return False

        # Obvious block starters
        if l.endswith('{') or l.startswith('{'):
            return True
        if l.startswith('('):
            return True

        # if/for/while/select/until/case
        if re.match(r'^\s*(if|for|while|select|until|case)\b', l):
            return True

        # Lines that contain "then" or "do" typically start blocks (if/for/while)
        if re.search(r'(^|[;\s])(then|do)\b', l):
            return True

        # case ... in
        if re.search(r'\bin\s*$', l) and re.match(r'^\s*case\b', l):
            return True

        # Function definitions
        # function name { ... } or name() { ... }
        if re.match(r'^\s*function\s+\w+(\s*\(\s*\))?\s*\{?$', l):
            return True
        if re.match(r'^\s*\w+\s*\(\s*\)\s*\{?$', l):
            return True

        return False

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        l = ShellUtils._strip_comments(line or "").strip()
        if not l:
            return False

        # Exact end keywords
        if l in {'fi', 'done', 'esac'}:
            return True

        # Block closers
        if l == '}' or l == ')':
            return True
        if l.endswith('}') or l.endswith(')'):
            return True

        # case clause terminators
        if l.endswith(';;') or l.endswith(';&') or l.endswith(';;&'):
            return True

        return False

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        s = ShellUtils._strip_comments(line or "")
        if not s:
            return False

        # Order matters: longer operators first
        ops = [
            '<<-', '<<<', '<<', '>>', '|&', '&&', '||', ';;&', ';&', ';;', '>|',
            '>&', '<&', '<>', '2>', '1>', '0>', ';', '|', '&', '>', '<'
        ]

        in_s = False
        in_d = False
        i = 0
        n = len(s)
        while i < n:
            ch = s[i]
            if ch == '\\':
                i += 2
                continue
            if not in_d and ch == "'" and not in_s:
                in_s = True
                i += 1
                continue
            if in_s:
                if ch == "'":
                    in_s = False
                i += 1
                continue
            if not in_s and ch == '"' and not in_d:
                in_d = True
                i += 1
                continue
            if in_d:
                if ch == '"':
                    in_d = False
                i += 1
                continue

            # Try to match any operator at position i
            for op in ops:
                if s.startswith(op, i):
                    return True
            i += 1

        return False

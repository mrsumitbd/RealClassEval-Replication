import re


class ShellUtils:
    """Utilities for processing shell commands within Makefile recipes."""

    _START_WORDS = {
        "if",
        "for",
        "while",
        "until",
        "case",
        "select",
        "then",
        "do",
        "else",
        "elif",
    }
    _END_WORDS = {"fi", "done", "esac"}

    @staticmethod
    def _strip_make_recipe_prefix(line: str) -> str:
        s = line.lstrip()
        while s and s[0] in "@+-":
            s = s[1:].lstrip()
        return s

    @staticmethod
    def _strip_comments(s: str) -> str:
        in_single = in_double = in_bt = False
        dollar_paren = 0
        brace_param = 0
        i = 0
        while i < len(s):
            ch = s[i]
            if ch == "\\" and not in_single:
                i += 2
                continue
            if in_single:
                if ch == "'":
                    in_single = False
                i += 1
                continue
            if in_double:
                if ch == '"':
                    in_double = False
                elif ch == "\\":
                    i += 2
                    continue
                i += 1
                continue
            if in_bt:
                if ch == "`":
                    in_bt = False
                i += 1
                continue
            # outside quotes
            if ch == "'":
                in_single = True
                i += 1
                continue
            if ch == '"':
                in_double = True
                i += 1
                continue
            if ch == "`":
                in_bt = True
                i += 1
                continue
            if ch == "$" and i + 1 < len(s) and s[i + 1] == "{":
                brace_param += 1
                i += 2
                continue
            if brace_param > 0:
                if ch == "{":
                    brace_param += 1
                elif ch == "}":
                    brace_param -= 1
                i += 1
                continue
            if ch == "$" and i + 1 < len(s) and s[i + 1] == "(":
                # $(...) or $((...))
                dollar_paren += 1
                i += 2
                continue
            if dollar_paren > 0:
                if ch == "(":
                    dollar_paren += 1
                elif ch == ")":
                    dollar_paren -= 1
                i += 1
                continue
            if ch == "#":
                return s[:i].rstrip()
            i += 1
        return s.rstrip()

    @staticmethod
    def _preprocess(line: str) -> str:
        return ShellUtils._strip_comments(ShellUtils._strip_make_recipe_prefix(line))

    @staticmethod
    def _first_word(code: str) -> str | None:
        # Extract the leading word token (letters, digits, underscores)
        m = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*)\b", code)
        return m.group(1) if m else None

    @staticmethod
    def _looks_like_function_def(code: str) -> bool:
        # function name [()] { ... } OR name() { ... }
        if re.match(r"\s*function\b", code):
            return True
        if re.match(r"\s*[A-Za-z_][A-Za-z0-9_]*\s*\(\s*\)", code):
            return True
        return False

    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        """Check if a line starts a shell control structure."""
        code = ShellUtils._preprocess(line)
        if not code:
            return False

        # Subshell or brace group start
        if code.lstrip().startswith("(") or code.lstrip().startswith("{"):
            return True

        if ShellUtils._looks_like_function_def(code):
            return True

        fw = ShellUtils._first_word(code)
        if fw and fw in ShellUtils._START_WORDS:
            return True

        return False

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        """Check if a line ends a shell control structure."""
        code = ShellUtils._preprocess(line)
        if not code:
            return False

        stripped = code.lstrip()

        # Closing tokens
        fw = ShellUtils._first_word(stripped)
        if fw and fw in ShellUtils._END_WORDS:
            return True

        # Closing of subshell or brace group
        if stripped.startswith(")") or stripped.startswith("}"):
            return True

        # Allow lines that end with only '}' or ');' etc.
        if stripped in ("}", ")", "};", ");"):
            return True

        return False

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        """Check if content contains shell operators that suggest deliberate structure."""
        code = ShellUtils._preprocess(line)
        if not code:
            return False

        # Keywords often indicate structure even if no operators
        fw = ShellUtils._first_word(code)
        if fw and (
            fw in ShellUtils._START_WORDS
            or fw in ShellUtils._END_WORDS
            or fw in {"function"}
        ):
            return True

        s = code
        in_single = in_double = in_bt = False
        dollar_paren = 0
        brace_param = 0
        i = 0
        while i < len(s):
            ch = s[i]

            # Escapes (not active in single quotes)
            if ch == "\\" and not in_single:
                i += 2
                continue

            # Inside single quotes
            if in_single:
                if ch == "'":
                    in_single = False
                i += 1
                continue

            # Inside double quotes
            if in_double:
                if ch == '"':
                    in_double = False
                elif ch == "\\":
                    i += 2
                    continue
                i += 1
                continue

            # Inside backticks
            if in_bt:
                if ch == "`":
                    in_bt = False
                i += 1
                continue

            # Enter quotes
            if ch == "'":
                in_single = True
                i += 1
                continue
            if ch == '"':
                in_double = True
                i += 1
                continue
            if ch == "`":
                in_bt = True
                i += 1
                continue

            # Parameter expansion ${...}
            if ch == "$" and i + 1 < len(s) and s[i + 1] == "{":
                brace_param += 1
                i += 2
                continue
            if brace_param > 0:
                if ch == "{":
                    brace_param += 1
                elif ch == "}":
                    brace_param -= 1
                i += 1
                continue

            # Command (or arithmetic) substitution $(...)
            if ch == "$" and i + 1 < len(s) and s[i + 1] == "(":
                return True  # $( is a strong operator signal

            if dollar_paren > 0:
                if ch == "(":
                    dollar_paren += 1
                elif ch == ")":
                    dollar_paren -= 1
                i += 1
                continue

            # Multi-char operators
            two = s[i: i + 2]
            three = s[i: i + 3]
            if two in {"&&", "||", ";;", "|&", ";&", ";&"}:
                return True
            if three == "<<<":
                return True
            if two in {"<<", ">>"}:
                return True

            # Single-char operators
            if ch in {";", "|", "&", ">", "<", "(", ")", "{", "}"}:
                return True

            i += 1

        return False

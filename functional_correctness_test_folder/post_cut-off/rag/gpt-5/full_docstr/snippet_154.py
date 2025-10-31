import re
from typing import Optional


class ShellUtils:
    """Utilities for processing shell commands within Makefile recipes."""

    @staticmethod
    def _strip_recipe_prefix(line: str) -> str:
        s = line.lstrip()
        while s and s[0] in "@+-":
            s = s[1:].lstrip()
        return s

    @staticmethod
    def _strip_comments_outside_quotes(s: str) -> str:
        out = []
        in_sq = False
        in_dq = False
        in_bt = False  # backticks
        escape = False
        for i, ch in enumerate(s):
            if escape:
                out.append(ch)
                escape = False
                continue
            if ch == "\\" and not in_sq:
                out.append(ch)
                escape = True
                continue
            if ch == "'" and not in_dq and not in_bt:
                in_sq = not in_sq
                out.append(ch)
                continue
            if ch == '"' and not in_sq and not in_bt:
                in_dq = not in_dq
                out.append(ch)
                continue
            if ch == "`" and not in_sq and not in_dq:
                in_bt = not in_bt
                out.append(ch)
                continue
            if ch == "#" and not in_sq and not in_dq and not in_bt:
                break
            out.append(ch)
        return "".join(out)

    @staticmethod
    def _remove_quoted_text(s: str) -> str:
        out = []
        in_sq = False
        in_dq = False
        in_bt = False
        escape = False
        for ch in s:
            if escape:
                out.append(" ")
                escape = False
                continue
            if ch == "\\" and not in_sq:
                out.append(" ")
                escape = True
                continue
            if ch == "'" and not in_dq and not in_bt:
                in_sq = not in_sq
                out.append(" ")
                continue
            if ch == '"' and not in_sq and not in_bt:
                in_dq = not in_dq
                out.append(" ")
                continue
            if ch == "`" and not in_sq and not in_dq:
                in_bt = not in_bt
                out.append(" ")
                continue
            out.append(" " if (in_sq or in_dq or in_bt) else ch)
        return "".join(out)

    @staticmethod
    def _remove_make_variables(s: str) -> str:
        out = []
        i = 0
        n = len(s)
        while i < n:
            ch = s[i]
            if ch == "$" and i + 1 < n and s[i + 1] in "({":
                open_ch = s[i + 1]
                close_ch = ")" if open_ch == "(" else "}"
                depth = 0
                # Skip the '$' and the opening bracket
                i += 2
                depth += 1
                # consume content until matching close, handling nesting
                while i < n:
                    c = s[i]
                    if c == open_ch:
                        depth += 1
                    elif c == close_ch:
                        depth -= 1
                        if depth == 0:
                            i += 1
                            break
                    i += 1
                # replace the whole variable with a placeholder to preserve spacing
                out.append(" ")
                continue
            out.append(ch)
            i += 1
        return "".join(out)

    @staticmethod
    def _preprocess(line: str) -> str:
        s = ShellUtils._strip_recipe_prefix(line)
        s = ShellUtils._strip_comments_outside_quotes(s)
        s = ShellUtils._remove_make_variables(s)
        s = ShellUtils._remove_quoted_text(s)
        return s.strip()

    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        """Check if a line starts a shell control structure."""
        s = ShellUtils._preprocess(line)
        if not s:
            return False

        # Common starts: if ...; then, then, for/while/until/select ...; do, do, case ... in
        if re.search(r'(^|\s)if\b.*\bthen\b', s):
            return True
        if re.match(r'^\s*then\b', s):
            return True
        if re.search(r'^(for|while|until|select)\b.*\bdo\b', s):
            return True
        if re.match(r'^\s*do\b', s):
            return True
        if re.match(r'^\s*case\b.*\bin\b', s):
            return True

        # Function definition: name() or name() {
        if re.match(r'^[A-Za-z_][A-Za-z0-9_]*\s*\(\s*\)\s*\{?\s*$', s):
            return True

        # Group starts: { ...  or ( ...  (treat unmatched open as start), or line ends with '{'
        if s.endswith("{"):
            return True
        # Unmatched '(' without a matching ')' and not part of process substitution
        if "(" in s and ")" not in s:
            return True
        # Starts with "{" or "("
        if re.match(r'^\s*[\{\(]\b?', s):
            return True

        return False

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        """Check if a line ends a shell control structure."""
        s = ShellUtils._preprocess(line)
        if not s:
            return False

        # Common ends: fi, done, esac (optionally followed by ';')
        if re.match(r'^(fi|done|esac)\b(?:\s*;?\s*)$', s):
            return True

        # Closing group tokens '}' or ')' on their own (optionally followed by ';')
        if re.match(r'^[\)\}]\s*;?\s*$', s):
            return True

        # Unmatched closing tokens: contains ')' without '(', or '}' without '{'
        if ")" in s and "(" not in s:
            # Avoid counting test subshells incorrectly; require that the ')' be at end or only followed by spaces/;.
            if re.search(r'\)\s*;?\s*$', s):
                return True
        if "}" in s and "{" not in s:
            if re.search(r'\}\s*;?\s*$', s):
                return True

        return False

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        """Check if content contains shell operators that suggest deliberate structure."""
        s = ShellUtils._preprocess(line)
        if not s:
            return False

        # Starts/ends of control structures imply operators
        if ShellUtils.is_shell_control_start(line) or ShellUtils.is_shell_control_end(line):
            return True

        # Logical and pipeline operators
        if "&&" in s or "||" in s:
            return True
        # Single pipe (not part of '||')
        if re.search(r'(^|[^|])\|([^|]|$)', s):
            return True
        # Semicolon separating commands (there is something after ';')
        if re.search(r';\s*\S', s):
            return True
        # Case item terminator ';;' or fall-through ';&' or ';;&'
        if re.search(r';;&|;&|;;', s):
            return True
        # Redirections and here-doc/strings
        if re.search(r'(\d?>&\d+)|(\d?>&-)|(\d?>&1)|[<>]{1,3}', s):
            return True
        # Background operator '&' (not part of '&&')
        if re.search(r'(^|\s)&(\s|$)', s) and "&&" not in s:
            return True

        return False

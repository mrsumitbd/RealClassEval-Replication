import re
from typing import Tuple


class ShellUtils:
    """Utilities for processing shell commands within Makefile recipes."""

    @staticmethod
    def _strip_make_prefix(line: str) -> str:
        s = line.lstrip()
        i = 0
        while i < len(s) and s[i] in "@-+":
            i += 1
        return s[i:].lstrip()

    @staticmethod
    def _remove_comments(s: str) -> str:
        out = []
        in_single = False
        in_double = False
        in_backtick = False
        escape = False
        for i, ch in enumerate(s):
            if escape:
                out.append(ch)
                escape = False
                continue
            if ch == "\\":
                # Backslash escapes inside double/backtick contexts; in single quotes it's literal.
                if not in_single:
                    escape = True
                out.append(ch)
                continue
            if ch == "'" and not in_double and not in_backtick:
                in_single = not in_single
                out.append(ch)
                continue
            if ch == '"' and not in_single and not in_backtick:
                in_double = not in_double
                out.append(ch)
                continue
            if ch == "`" and not in_single and not in_double:
                in_backtick = not in_backtick
                out.append(ch)
                continue
            if ch == "#" and not (in_single or in_double or in_backtick):
                # Comment starts: discard rest
                break
            out.append(ch)
        return "".join(out)

    @staticmethod
    def _mask_quoted(s: str) -> str:
        # Replace characters within quotes with spaces (to preserve indices)
        out = []
        in_single = False
        in_double = False
        in_backtick = False
        escape = False
        for ch in s:
            if escape:
                out.append(" ")
                escape = False
                continue
            if ch == "\\":
                if not in_single:
                    escape = True
                out.append(" ")
                continue
            if ch == "'" and not in_double and not in_backtick:
                in_single = not in_single
                out.append(" ")
                continue
            if ch == '"' and not in_single and not in_backtick:
                in_double = not in_double
                out.append(" ")
                continue
            if ch == "`" and not in_single and not in_double:
                in_backtick = not in_backtick
                out.append(" ")
                continue
            if in_single or in_double or in_backtick:
                out.append(" ")
            else:
                out.append(ch)
        return "".join(out)

    @staticmethod
    def _prep(line: str) -> str:
        s = ShellUtils._strip_make_prefix(line)
        s = ShellUtils._remove_comments(s)
        s = s.strip()
        return s

    @staticmethod
    def _clean_for_scan(line: str) -> str:
        return ShellUtils._mask_quoted(ShellUtils._prep(line))

    @staticmethod
    def _word_count(s: str, word: str) -> int:
        return len(re.findall(rf"\b{word}\b", s))

    @staticmethod
    def _has_word(s: str, word: str) -> bool:
        return ShellUtils._word_count(s, word) > 0

    @staticmethod
    def _count_braces(s: str) -> Tuple[int, int]:
        # Count grouping braces { } as standalone tokens (avoid ${...} and brace expansion heuristically)
        open_count = len(re.findall(r"(^|\s)\{(\s|$|;)", s))
        close_count = len(re.findall(r"(^|\s)\}(\s|$|;)", s))
        return open_count, close_count

    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        """Check if a line starts a shell control structure."""
        s = ShellUtils._clean_for_scan(line)
        if not s:
            return False

        # Single-line immediate starters that don't necessarily include an opener keyword on the same line
        # but which open a block body.
        if ShellUtils._has_word(s, "then") and not ShellUtils._has_word(s, "fi"):
            return True
        if ShellUtils._has_word(s, "do") and not ShellUtils._has_word(s, "done"):
            return True
        if ShellUtils._has_word(s, "elif") and not ShellUtils._has_word(s, "fi"):
            return True
        if ShellUtils._has_word(s, "else") and not ShellUtils._has_word(s, "fi"):
            return True

        # case ... in starts a control structure
        if re.search(r"\bcase\b.*\bin\b", s) and not ShellUtils._has_word(s, "esac"):
            return True

        # function keyword or name() { patterns
        if ShellUtils._has_word(s, "function"):
            # Often followed by a block; treat as start unless immediately closed.
            opens, closes = ShellUtils._count_braces(s)
            if opens > closes:
                return True

        # Block openers and closers
        open_kw = 0
        for w in ("if", "for", "while", "until", "case", "select"):
            # Exclude 'elif' from counting towards 'if'
            if w == "if":
                # still counts, but this avoids double-start on same line
                open_kw += len(re.findall(r"\bif\b(?!\s*;?\s*then\b)", s))
                # Count 'if' regardless of then; it's an opener conceptually.
                open_kw = ShellUtils._word_count(
                    s, "if") + (open_kw - ShellUtils._word_count(s, "if"))
            else:
                open_kw += ShellUtils._word_count(s, w)

        close_kw = 0
        for w in ("fi", "done", "esac"):
            close_kw += ShellUtils._word_count(s, w)

        # Count grouping braces { }
        opens, closes = ShellUtils._count_braces(s)
        delta = open_kw - close_kw + (opens - closes)

        if delta > 0:
            return True

        # Function-style open without 'function' keyword: name() {
        if re.search(r"\b[A-Za-z_]\w*\s*\(\)\s*\{", s):
            return True

        return False

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        """Check if a line ends a shell control structure."""
        s = ShellUtils._clean_for_scan(line)
        if not s:
            return False

        # Keywords that close blocks
        if any(ShellUtils._has_word(s, w) for w in ("fi", "done", "esac")):
            return True

        # else/elif close the preceding then-body
        if ShellUtils._has_word(s, "else") or ShellUtils._has_word(s, "elif"):
            return True

        # End of case clause or grouped block
        if ";;" in s:
            return True

        # Closing brace for grouped commands or function bodies
        opens, closes = ShellUtils._count_braces(s)
        if closes > opens:
            return True
        # Lines that are just a closing brace or have a closing brace at end
        if re.search(r"(^|\s)\}(\s|$|;)", s):
            return True

        return False

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        """Check if content contains shell operators that suggest deliberate structure."""
        s = ShellUtils._clean_for_scan(line)
        if not s:
            return False

        # Control keywords
        keyword_pattern = re.compile(
            r"\b(if|then|else|elif|fi|for|while|until|do|done|case|esac|select|function)\b"
        )
        if keyword_pattern.search(s):
            return True

        # Common operator tokens (outside quotes)
        operator_patterns = [
            r"\&\&",
            r"\|\|",
            r"\|&",
            r"\|",
            r";;",
            r";",
            r"\(\s*",   # opening subshell/grouping paren
            r"\s*\)",   # closing paren
            r"(^|\s)\{",  # grouping brace open
            r"\}(\s|$|;)",  # grouping brace close
            r">>>",
            r"<<-",
            r"<<<?",
            r">>",
            r">\|",
            r"&>",
            r"2>|?",
            r"\s<\s?",
            r"\s>\s?",
        ]
        for pat in operator_patterns:
            if re.search(pat, s):
                return True

        # Command substitution
        if "$(" in s:
            return True

        # Backticks for command substitution
        if "`" in ShellUtils._prep(line):
            # If backticks survived cleaning, they're outside quotes
            return True

        return False

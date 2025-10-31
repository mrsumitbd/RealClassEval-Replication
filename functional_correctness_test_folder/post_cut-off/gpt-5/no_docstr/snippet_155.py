from typing import Optional

import re


class PatternUtils:
    _assign_ops = ("::=", ":=", "?=", "+=", "=")

    @staticmethod
    def contains_assignment(line: str) -> bool:
        if not line:
            return False
        # Ignore pure comments and recipe lines
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#") or stripped.startswith("\t"):
            return False

        # Strip trailing comment for detection
        code = stripped.split("#", 1)[0]

        # Detect top-level assignment operators (longest-first)
        for op in PatternUtils._assign_ops:
            idx = code.find(op)
            if idx == -1:
                continue
            # Ensure we have something on LHS (non-empty after stripping whitespace)
            lhs = code[:idx].rstrip()
            if not lhs:
                continue

            # Heuristic: avoid treating target rules as assignment
            # - if the op is '=' (single) and there's a ':' before it that is not part of ':='/'::=' it's likely a rule
            if op == "=":
                colon_idx = code.find(":")
                if colon_idx != -1 and colon_idx < idx:
                    # if it's ':=' or '::=' it would have matched earlier ops
                    return False

            return True

        return False

    @staticmethod
    def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
        if not line:
            return line

        # Keep leading indentation and trailing comment
        leading_ws_match = re.match(r"^(\s*)", line)
        leading_ws = leading_ws_match.group(1) if leading_ws_match else ""
        rest = line[len(leading_ws):]

        # Separate comment (but not in recipe lines)
        if rest.startswith("\t"):
            return line

        parts = rest.split("#", 1)
        code = parts[0]
        comment = "" if len(parts) == 1 else "#" + parts[1]

        # Try to locate the first assignment operator (longest-first)
        pos = -1
        op_found = None
        for op in PatternUtils._assign_ops:
            pos = code.find(op)
            if pos != -1:
                op_found = op
                break

        if op_found is None:
            return line

        lhs = code[:pos].rstrip()
        rhs = code[pos + len(op_found):].lstrip()

        if not lhs:
            return line

        sep = f" {op_found} " if use_spaces else op_found
        new_code = f"{lhs}{sep}{rhs}"

        return f"{leading_ws}{new_code}{comment}"

    @staticmethod
    def format_target_colon(line: str, space_before: bool = False, space_after: bool = True) -> Optional[str]:
        if not line:
            return None

        stripped = line.lstrip()
        if stripped.startswith("#") or stripped.startswith("\t"):
            return None

        # Do not touch variable assignments
        if PatternUtils.contains_assignment(line):
            return None

        # Find the first colon or double-colon that indicates rule separator
        # Exclude ':=' or '::=' already filtered by contains_assignment
        m = re.search(r":{1,2}", line)
        if not m:
            return None

        # Determine colon token
        start, end = m.start(), m.end()
        colon_token = line[start:end]

        # Build new spacing around the colon token
        left = line[:start].rstrip()
        right = line[end:].lstrip()

        before = " " if space_before else ""
        after = " " if space_after else ""

        new_line = f"{left}{before}{colon_token}{after}{right}"
        return new_line

    @staticmethod
    def format_pattern_rule(line: str, space_after_colon: bool = True) -> Optional[str]:
        if not line:
            return None

        stripped = line.lstrip()
        if stripped.startswith("#") or stripped.startswith("\t"):
            return None

        # Not an assignment
        if PatternUtils.contains_assignment(line):
            return None

        # Identify a colon that separates target from prerequisites
        m = re.search(r":{1,2}", line)
        if not m:
            return None

        # Check that target part contains a '%' (pattern rule)
        target_part = line[: m.start()]
        if "%" not in target_part:
            return None

        # Reformat spacing: no space before colon for pattern rules by default,
        # configurable space after colon.
        left = target_part.rstrip()
        colon_token = line[m.start(): m.end()]
        right = line[m.end():].lstrip()

        after = " " if space_after_colon else ""
        new_line = f"{left}{colon_token}{after}{right}"
        return new_line

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        if not line:
            return False
        s = line.lstrip()
        if s.startswith("#"):
            return False
        return re.match(r"^(ifeq|ifneq|ifdef|ifndef|else|endif)\b", s) is not None

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        if not PatternUtils.is_conditional_directive(line):
            return 0
        s = line.lstrip()
        if re.match(r"^endif\b", s):
            return -1
        if re.match(r"^else\b", s):
            return 0
        if re.match(r"^(ifeq|ifneq|ifdef|ifndef)\b", s):
            return 1
        return 0

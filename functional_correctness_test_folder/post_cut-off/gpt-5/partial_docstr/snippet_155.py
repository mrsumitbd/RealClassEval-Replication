from typing import Optional
import re


class PatternUtils:

    @staticmethod
    def contains_assignment(line: str) -> bool:
        if not line:
            return False
        s = line.lstrip()
        if s.startswith('#') or s.startswith('\t'):
            return False
        # Match a Make variable assignment at beginning of non-comment line
        # VAR =, VAR:=, VAR?=, VAR+=
        return re.match(r'^[A-Za-z_][A-Za-z0-9_.-]*\s*(?:\+|:|\?)?=', s) is not None

    @staticmethod
    def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
        if not PatternUtils.contains_assignment(line):
            return line

        # Preserve trailing comment
        parts = re.split(r'(?<!\\)#', line, maxsplit=1)
        code = parts[0].rstrip()
        comment = '' if len(parts) == 1 else '#' + parts[1]

        m = re.match(
            r'^(\s*)([A-Za-z_][A-Za-z0-9_.-]*)(\s*)((?:\+|:|\?)?=)(\s*)(.*)$', code)
        if not m:
            return line
        lead, var, pre_op_space, op, post_op_space, value = m.groups()

        if use_spaces:
            new_code = f"{lead}{var} {op} {value.strip()}"
        else:
            new_code = f"{lead}{var}{op}{value.strip()}"

        result = new_code + ('' if comment == '' else ' ' + comment if not new_code.endswith(
            ' ') and not comment.startswith(' ') else comment)
        return result

    @staticmethod
    def format_target_colon(line: str, space_before: bool = False, space_after: bool = True) -> Optional[str]:
        '''
        Format colon spacing in target definitions.
        Args:
            line: The line to format
            space_before: Whether to add space before colon
            space_after: Whether to add space after colon
        Returns:
            Formatted line or None if no changes needed
        '''
        if not line or line.lstrip().startswith('#') or line.startswith('\t'):
            return None
        if PatternUtils.contains_assignment(line):
            return None

        # Split off trailing comment
        parts = re.split(r'(?<!\\)#', line, maxsplit=1)
        code = parts[0].rstrip('\n')
        comment = '' if len(parts) == 1 else '#' + parts[1]

        # Find first colon that denotes a target definition (single or double colon)
        idx = code.find(':')
        if idx == -1:
            return None

        # Determine if it's double-colon
        colon_len = 2 if idx + 1 < len(code) and code[idx + 1] == ':' else 1

        left = code[:idx]
        right = code[idx + colon_len:]

        new_left = left.rstrip()
        new_right = right.lstrip()

        before = ' ' if space_before and (not new_left.endswith(' ')) else ''
        after = ' ' if space_after and (not new_right.startswith(' ') and len(
            new_right) > 0) else (' ' if space_after and len(new_right) == 0 else '')

        new_code = f"{new_left}{before}{':' * colon_len}{after}{new_right}"

        # If nothing changed, return None
        if new_code == code:
            return None

        # Reattach comment with proper spacing if needed
        if comment:
            if not new_code.endswith(' ') and not comment.startswith(' '):
                new_code += ' ' + comment
            else:
                new_code += comment
        return new_code

    @staticmethod
    def format_pattern_rule(line: str, space_after_colon: bool = True) -> Optional[str]:
        if not line or line.lstrip().startswith('#') or line.startswith('\t'):
            return None
        if PatternUtils.contains_assignment(line):
            return None

        # A simple heuristic for pattern rule: '%' before the first colon
        parts = re.split(r'(?<!\\)#', line, maxsplit=1)
        code = parts[0].rstrip('\n')
        comment = '' if len(parts) == 1 else '#' + parts[1]

        idx = code.find(':')
        if idx == -1:
            return None
        if '%' not in code[:idx]:
            return None

        # Use target colon formatter with no space before, configurable after
        formatted = PatternUtils.format_target_colon(
            code, space_before=False, space_after=space_after_colon)
        if formatted is None:
            return None

        if comment:
            if not formatted.endswith(' ') and not comment.startswith(' '):
                formatted += ' ' + comment
            else:
                formatted += comment
        return formatted

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        if not line:
            return False
        s = line.lstrip()
        if s.startswith('#'):
            return False
        return re.match(r'^(ifeq|ifneq|ifdef|ifndef|else|endif)\b', s) is not None

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        '''
        Get the appropriate indentation level for conditional directives.
        Args:
            line: The conditional directive line
        Returns:
            Number of spaces for indentation
        '''
        if not PatternUtils.is_conditional_directive(line):
            return 0
        # Align all conditional directives to column 0
        return 0

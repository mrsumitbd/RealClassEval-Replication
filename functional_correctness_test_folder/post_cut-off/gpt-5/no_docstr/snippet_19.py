import re
from typing import List, Tuple


class MarkdownCleaner:
    @staticmethod
    def _replace_inline_dollar(m: re.Match) -> str:
        return m.group(1).strip()

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        block = match.group(0)
        lines = [l.rstrip() for l in block.strip("\n").splitlines()]
        if len(lines) < 2:
            return block

        sep_re = re.compile(
            r'^\s*\|?\s*:?-{2,}:?\s*(?:\|\s*:?-{2,}:?\s*)+\|?\s*$')
        cleaned_lines: List[str] = []
        skipped_sep = False
        for idx, line in enumerate(lines):
            if not skipped_sep and sep_re.match(line):
                skipped_sep = True
                continue
            cleaned_lines.append(line)

        def split_cells(line: str) -> str:
            s = line.strip()
            if s.startswith("|"):
                s = s[1:]
            if s.endswith("|"):
                s = s[:-1]
            cells = [c.strip() for c in s.split("|")]
            return "\t".join(cells)

        rows = [split_cells(l) for l in cleaned_lines if "|" in l]
        return "\n".join(rows)

    @staticmethod
    def clean_markdown(text: str) -> str:
        if not text:
            return text

        # Normalize newlines
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Protect fenced code blocks
        fenced_pattern = re.compile(r'```.*?```', re.DOTALL)
        fenced_blocks: List[str] = []

        def _store_fenced(m: re.Match) -> str:
            fenced_blocks.append(m.group(0))
            return f"__FENCED_CODE_BLOCK_{len(fenced_blocks)-1}__"

        text = fenced_pattern.sub(_store_fenced, text)

        # Protect inline code
        inline_code_pattern = re.compile(r'`[^`\n]*`')
        inline_blocks: List[str] = []

        def _store_inline(m: re.Match) -> str:
            inline_blocks.append(m.group(0))
            return f"__INLINE_CODE_{len(inline_blocks)-1}__"

        text = inline_code_pattern.sub(_store_inline, text)

        # Replace markdown tables with TSV-like representation
        table_block_pattern = re.compile(
            r'(?m)^(?:\s*\|.*)\n\s*\|?\s*:?-{2,}:?\s*(?:\|\s*:?-{2,}:?\s*)+\|?\s*\n(?:\s*\|.*\n?)+'
        )
        text = table_block_pattern.sub(
            MarkdownCleaner._replace_table_block, text)

        # Replace block math $$...$$ with its content (multiline)
        block_math_pattern = re.compile(r'(?<!\\)\$\$(.+?)\$\$', re.DOTALL)
        text = block_math_pattern.sub(lambda m: m.group(1).strip(), text)

        # Replace inline $...$ with its content, not crossing newlines
        inline_math_pattern = re.compile(
            r'(?<!\\)\$(?!\$)([^\n]*?)(?<!\\)\$', re.MULTILINE)
        text = inline_math_pattern.sub(
            MarkdownCleaner._replace_inline_dollar, text)

        # Restore inline code
        def _restore_inline(m: re.Match) -> str:
            idx = int(m.group(1))
            return inline_blocks[idx]

        text = re.sub(r'__INLINE_CODE_(\d+)__', _restore_inline, text)

        # Restore fenced code
        def _restore_fenced(m: re.Match) -> str:
            idx = int(m.group(1))
            return fenced_blocks[idx]

        text = re.sub(r'__FENCED_CODE_BLOCK_(\d+)__', _restore_fenced, text)

        return text.strip()

import re
from typing import List


class MarkdownCleaner:

    @staticmethod
    def _replace_inline_dollar(m: re.Match) -> str:
        '''
        只要捕获到完整的 "$...$":
          - 如果内部有典型公式字符 => 去掉两侧 $
          - 否则 (纯数字/货币等) => 保留 "$...$"
        '''
        inner = m.group(1).strip()
        # 典型公式/LaTeX迹象
        mathy = re.compile(
            r'(\\[A-Za-z]+|[\^_{}]|\\left|\\right|\\sum|\\int|\\frac|\\sqrt|\\times|\\cdot|\\pi|\\alpha|\\beta|\\gamma|=|<|>)'
        )
        if mathy.search(inner):
            return inner
        return m.group(0)

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        block = match.group(0)
        lines = [ln.rstrip() for ln in block.strip('\n').splitlines()]
        if len(lines) < 2:
            return block

        # Skip the separator line and strip leading/trailing pipes
        def split_row(row: str) -> List[str]:
            row = row.strip()
            if row.startswith('|'):
                row = row[1:]
            if row.endswith('|'):
                row = row[:-1]
            return [c.strip() for c in row.split('|')]

        cleaned_lines: List[str] = []
        for idx, ln in enumerate(lines):
            # skip the alignment/separator line
            if idx == 1:
                continue
            # Heuristic: if the line looks like a separator, skip it too
            if re.fullmatch(r'[ \t|\-:]+', ln or ''):
                continue
            cells = split_row(ln)
            # remove entirely empty rows
            if all(c == '' for c in cells):
                continue
            cleaned_lines.append('  '.join(cells))
        return '\n'.join(cleaned_lines) + '\n'

    @staticmethod
    def clean_markdown(text: str) -> str:
        '''
        主入口方法：依序执行所有正则，移除或替换 Markdown 元素
        '''
        if not text:
            return ''

        # Normalize newlines
        s = text.replace('\r\n', '\n').replace('\r', '\n')

        # Remove fenced code fences but keep content
        fence_pattern = re.compile(
            r'(^|\n)```[^\n]*\n(.*?)(\n```)(?=\n|$)', re.DOTALL)
        s = fence_pattern.sub(lambda m: f"{m.group(1)}{m.group(2)}", s)

        # Inline code `code` -> code
        s = re.sub(r'`([^`]+)`', r'\1', s)

        # Images ![alt](url) -> alt
        s = re.sub(r'!\[([^\]]*)\]\((?:[^)]+)\)', r'\1', s)

        # Links [text](url) -> text
        s = re.sub(r'\[([^\]]+)\]\((?:[^)]+)\)', r'\1', s)

        # Tables -> plain lines (via block)
        table_block = re.compile(
            r'(?:(?<=\n)|^)'                    # start of text or line
            r'(?:[ \t]*\|?.+\|?[ \t]*\n)'       # header line
            r'[ \t]*\|?(?:[ \t]*:?-{3,}:?[ \t]*\|)+[ \t]*(?:\n|$)'  # separator
            r'(?:[ \t]*\|?.+\|?[ \t]*(?:\n|$))+'                    # rows
        )
        s = table_block.sub(MarkdownCleaner._replace_table_block, s)

        # Headings: # ... -> text
        s = re.sub(r'^[ \t]{0,3}#{1,6}[ \t]+(.+)$',
                   r'\1', s, flags=re.MULTILINE)

        # Blockquotes: > text -> text
        s = re.sub(r'^[ \t]*>+[ \t]?(.*)$', r'\1', s, flags=re.MULTILINE)

        # Lists: unordered and ordered, remove markers
        s = re.sub(r'^[ \t]*[-+*][ \t]+', '', s, flags=re.MULTILINE)
        s = re.sub(r'^[ \t]*\d+[.)][ \t]+', '', s, flags=re.MULTILINE)

        # Horizontal rules: remove lines of --- *** ___
        s = re.sub(r'^[ \t]*(-{3,}|\*{3,}|_{3,})[ \t]*$',
                   '', s, flags=re.MULTILINE)

        # Emphasis/strong/strike: remove markers
        s = re.sub(r'(\*\*\*|___)(.+?)\1', r'\2', s)  # bold+italic
        s = re.sub(r'(\*\*|__)(.+?)\1', r'\2', s)     # bold
        s = re.sub(r'(\*|_)(.+?)\1', r'\2', s)        # italic
        s = re.sub(r'~~(.+?)~~', r'\1', s)            # strikethrough

        # Display math $$...$$ -> content
        s = re.sub(r'\$\$(.+?)\$\$', lambda m: m.group(1), s, flags=re.DOTALL)

        # Inline math $...$ -> maybe strip dollars
        inline_dollar = re.compile(r'\$(?!\$)(.+?)(?<!\\)\$')
        s = inline_dollar.sub(MarkdownCleaner._replace_inline_dollar, s)

        # Remove simple HTML tags (keep text)
        s = re.sub(r'</?[^>\n]+>', '', s)

        # Collapse excessive blank lines
        s = re.sub(r'[ \t]+\n', '\n', s)
        s = re.sub(r'\n{3,}', '\n\n', s)

        return s.strip('\n') + ('\n' if s.endswith('\n') else '')

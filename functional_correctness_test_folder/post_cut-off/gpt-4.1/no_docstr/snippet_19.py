
import re


class MarkdownCleaner:

    @staticmethod
    def _replace_inline_dollar(m: re.Match) -> str:
        content = m.group(1)
        # Remove leading/trailing whitespace inside the dollar
        content = content.strip()
        return f"${content}$"

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        table = match.group(0)
        # Remove leading/trailing whitespace on each line and remove trailing spaces
        lines = [line.rstrip() for line in table.strip().split('\n')]
        # Remove any empty lines at the start or end
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        return '\n'.join(lines) + '\n'

    @staticmethod
    def clean_markdown(text: str) -> str:
        # Clean up inline math: $ ... $ (not $$ ... $$)
        # Replace $   ...   $ with $...$
        text = re.sub(r'\$(\s*[^$][^$]*?\s*)\$',
                      MarkdownCleaner._replace_inline_dollar, text)
        # Clean up tables: lines starting and ending with |, possibly with --- separator
        # Find table blocks (at least two lines, all starting and ending with |)

        def table_block_iter(text):
            lines = text.split('\n')
            i = 0
            n = len(lines)
            while i < n:
                if re.match(r'^\s*\|.*\|\s*$', lines[i]):
                    start = i
                    while i < n and re.match(r'^\s*\|.*\|\s*$', lines[i]):
                        i += 1
                    if i - start >= 2:
                        yield (start, i)
                    else:
                        i += 1
                else:
                    i += 1

        # Replace table blocks
        lines = text.split('\n')
        table_spans = list(table_block_iter(text))
        offset = 0
        for start, end in table_spans:
            table_text = '\n'.join(lines[start:end])
            cleaned = MarkdownCleaner._replace_table_block(
                re.match(r'[\s\S]+', table_text))
            lines[start:end] = [cleaned.rstrip('\n')]
        text = '\n'.join(lines)
        return text

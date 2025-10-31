
import re


class MarkdownCleaner:

    @staticmethod
    def _replace_inline_dollar(m: re.Match) -> str:
        content = m.group(1)
        return f'${content}$'

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        table_content = match.group(1)
        lines = table_content.split('\n')
        cleaned_lines = []
        for line in lines:
            if line.startswith('|') and line.endswith('|'):
                cleaned_line = line.strip()
                cleaned_lines.append(cleaned_line)
        return '\n'.join(cleaned_lines) + '\n'

    @staticmethod
    def clean_markdown(text: str) -> str:
        # Replace inline $$...$$ with $...$
        text = re.sub(
            r'\$\$(.*?)\$\$', MarkdownCleaner._replace_inline_dollar, text, flags=re.DOTALL)

        # Clean table blocks
        text = re.sub(r'

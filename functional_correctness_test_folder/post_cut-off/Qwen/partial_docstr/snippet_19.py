
import re


class MarkdownCleaner:

    @staticmethod
    def _replace_inline_dollar(m: re.Match) -> str:
        content = m.group(1)
        if re.search(r'[a-zA-Z\(\)\[\]\{\}\\\/]', content):
            return content
        return m.group(0)

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        return ''

    @staticmethod
    def clean_markdown(text: str) -> str:
        # Replace inline dollar signs
        text = re.sub(
            r'\$(.*?)\$', MarkdownCleaner._replace_inline_dollar, text)
        # Remove table blocks
        text = re.sub(r'\|.*?\|\n(?:\|.*?\|\n)*',
                      MarkdownCleaner._replace_table_block, text, flags=re.DOTALL)
        return text

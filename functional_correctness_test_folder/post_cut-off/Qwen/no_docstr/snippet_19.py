
import re


class MarkdownCleaner:

    @staticmethod
    def _replace_inline_dollar(m: re.Match) -> str:
        return f"${m.group(1)}$"

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        return match.group(0).replace('|', ' | ')

    @staticmethod
    def clean_markdown(text: str) -> str:
        # Replace inline dollar signs
        text = re.sub(
            r'\$(.*?)\$', MarkdownCleaner._replace_inline_dollar, text)
        # Replace table blocks to ensure proper spacing
        text = re.sub(r'(\|.*?\|)', MarkdownCleaner._replace_table_block, text)
        return text

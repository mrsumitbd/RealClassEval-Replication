
import re


class MarkdownCleaner:

    @staticmethod
    def _replace_inline_dollar(m: re.Match) -> str:
        return m.group(1)

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        return match.group(1)

    @staticmethod
    def clean_markdown(text: str) -> str:
        # Replace inline dollar signs
        text = re.sub(
            r'\$(.*?)\$', MarkdownCleaner._replace_inline_dollar, text)
        # Replace table blocks
        text = re.sub(
            r'(\|.*?\|)', MarkdownCleaner._replace_table_block, text, flags=re.DOTALL)
        return text

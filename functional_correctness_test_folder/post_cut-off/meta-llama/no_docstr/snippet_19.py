
import re


class MarkdownCleaner:

    @staticmethod
    def _replace_inline_dollar(m: re.Match) -> str:
        """Replace inline dollar signs with escaped dollar signs."""
        return m.group(0).replace('$', '\$')

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        """Replace table block with its escaped version."""
        table_block = match.group(0)
        table_block = table_block.replace('|', '\|')
        return table_block

    @staticmethod
    def clean_markdown(text: str) -> str:
        """Clean markdown text by escaping certain characters."""
        # Escape inline dollar signs
        text = re.sub(r'(?<!\\)\$(.*?)(?<!\\)\$',
                      MarkdownCleaner._replace_inline_dollar, text)

        # Escape table blocks
        text = re.sub(
            r'(^\|.*\|$\n?)+', MarkdownCleaner._replace_table_block, text, flags=re.MULTILINE)

        return text

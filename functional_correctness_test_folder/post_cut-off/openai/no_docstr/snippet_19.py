
import re


class MarkdownCleaner:
    """
    Utility class for cleaning Markdown text.
    It removes inline math expressions wrapped in dollar signs
    and strips out Markdown tables.
    """

    @staticmethod
    def _replace_inline_dollar(m: re.Match) -> str:
        """
        Replace an inline dollar expression `$...$` with its inner content.
        """
        # Return the captured group (the content inside the dollar signs)
        return m.group(1)

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        """
        Remove an entire Markdown table block.
        """
        # The whole table block is discarded
        return ""

    @staticmethod
    def clean_markdown(text: str) -> str:
        """
        Clean the provided Markdown text by:
        1. Removing inline math expressions wrapped in `$...$`.
        2. Removing Markdown tables.
        """
        # 1. Remove inline dollar expressions
        #   Pattern: $...$ (non-greedy)
        text = re.sub(
            r'\$(.+?)\$', MarkdownCleaner._replace_inline_dollar, text)

        # 2. Remove Markdown tables
        #   A simple heuristic: a table starts with a line that contains
        #   at least one pipe `|` and is followed by one or more lines
        #   that also start with `|`.  We remove all consecutive lines
        #   that match this pattern.
        table_pattern = re.compile(
            r'(?m)^(?:\|.*\n)+\|.*\n?',  # match one or more table rows
            flags=re.MULTILINE
        )
        text = table_pattern.sub(MarkdownCleaner._replace_table_block, text)

        return text

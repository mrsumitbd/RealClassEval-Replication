
import re


class MarkdownCleaner:

    @staticmethod
    def _replace_inline_dollar(m: re.Match) -> str:
        content = m.group(1)
        formula_chars = {'=', '+', '-', '*', '/',
            '(', ')', '[', ']', '{', '}', '\\', '^', '_'}
        if any(char in content for char in formula_chars):
            return content
        else:
            return f'${content}$'

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        return ''

    @staticmethod
    def clean_markdown(text: str) -> str:
        # Remove inline code blocks
        text = re.sub(r'`([^`]+)`', r'\1', text)

        # Remove code blocks
        text = re.sub(r'

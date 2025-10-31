
import re


class MarkdownCleaner:

    @staticmethod
    def _replace_inline_dollar(m: re.Match) -> str:
        content = m.group(1)
        if any(char in content for char in {'_', '^', '\\', '{', '}', '(', ')', '[', ']', '|', ':', ';', '!', '?', '~', '`', '@', '#', '%', '&', '*', '+', '=', '<', '>', '/'}):
            return content
        else:
            return m.group(0)

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        return ''

    @staticmethod
    def clean_markdown(text: str) -> str:
        # 替换内联数学公式
        text = re.sub(r'\$([^$]+)\$',
                      MarkdownCleaner._replace_inline_dollar, text)
        # 移除表格
        text = re.sub(r'\|.*\|.*\n\|.*\|.*\n',
                      MarkdownCleaner._replace_table_block, text)
        return text

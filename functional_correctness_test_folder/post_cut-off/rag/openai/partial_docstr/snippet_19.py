
import re
from typing import Match


class MarkdownCleaner:
    """
    封装 Markdown 清理逻辑：直接用 MarkdownCleaner.clean_markdown(text) 即可
    """

    @staticmethod
    def _replace_inline_dollar(m: Match) -> str:
        """
        只要捕获到完整的 "$...$":
          - 如果内部有典型公式字符 => 去掉两侧 $
          - 否则 (纯数字/货币等) => 保留 "$...$"
        """
        content = m.group(1)
        # 典型公式字符：字母、运算符、括号等
        if re.search(r"[a-zA-Z+\-*/^=()\\]", content):
            return content
        return m.group(0)

    @staticmethod
    def _replace_table_block(match: Match) -> str:
        """
        当匹配到一个整段表格块时，回调该函数。
        这里直接删除整个表格块。
        """
        return ""

    @staticmethod
    def clean_markdown(text: str) -> str:
        """
        主入口方法：依序执行所有正则，移除或替换 Markdown 元素
        """
        # 1. 删除表格块
        table_pattern = r"\n?(\|.*\n)+\n?(\|.*\n)+"
        text = re.sub(
            table_pattern, MarkdownCleaner._replace_table_block, text, flags=re.MULTILINE)

        # 2. 删除代码块（

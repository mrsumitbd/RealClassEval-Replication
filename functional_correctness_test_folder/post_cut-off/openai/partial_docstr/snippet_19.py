
import re
from typing import Match


class MarkdownCleaner:
    @staticmethod
    def _replace_inline_dollar(m: Match) -> str:
        """
        只要捕获到完整的 "$...$":
          - 如果内部有典型公式字符 => 去掉两侧 $
          - 否则 (纯数字/货币等) => 保留 "$...$"
        """
        content = m.group(1)
        # 典型公式字符：字母、希腊字母、运算符、括号等
        if re.search(r'[A-Za-z0-9\+\-\*/\^=(){}\[\]α-ωΑ-Ω]', content):
            return content
        return f"${content}$"

    @staticmethod
    def _replace_table_block(match: Match) -> str:
        """
        删除 Markdown 表格块
        """
        return ""

    @staticmethod
    def clean_markdown(text: str) -> str:
        """
        主入口方法：依序执行所有正则，移除或替换 Markdown 元素
        """
        # 1. 代码块（fenced）
        text = re.sub(r'

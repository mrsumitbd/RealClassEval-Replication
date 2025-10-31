
import re


class MarkdownCleaner:
    '''
    封装 Markdown 清理逻辑：直接用 MarkdownCleaner.clean_markdown(text) 即可
    '''
    @staticmethod
    def _replace_inline_dollar(m: re.Match) -> str:
        '''
        只要捕获到完整的 "$...$":
          - 如果内部有典型公式字符 => 去掉两侧 $
          - 否则 (纯数字/货币等) => 保留 "$...$"
        '''
        content = m.group(1)
        # 典型公式字符集合
        formula_chars = set(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-*/^=()[]{}\\|\\$%#@&~<>")
        # 如果包含至少一个非数字/非空格字符且不是纯数字/货币符号
        if any(ch in formula_chars for ch in content) and not re.fullmatch(r'\d+(\.\d+)?', content):
            return content
        return f"${content}$"

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        '''
        当匹配到一个整段表格块时，回调该函数。
        '''
        # 直接删除整段表格
        return ''

    @staticmethod
    def clean_markdown(text: str) -> str:
        '''
        主入口方法：依序执行所有正则，移除或替换 Markdown 元素
        '''
        # 1. 删除代码块（

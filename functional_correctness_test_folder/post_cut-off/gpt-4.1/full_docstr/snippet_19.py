
import re


class MarkdownCleaner:
    '''
    封装 Markdown 清理逻辑：直接用 MarkdownCleaner.clean_markdown(text) 即可
    '''
    # 典型公式字符集合
    _formula_chars = set(
        '=+-*/^_\\{}[]()|<>αβγδεζηθικλμνξοπρστυφχψωABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')

    @staticmethod
    def _replace_inline_dollar(m: re.Match) -> str:
        '''
        只要捕获到完整的 "$...$":
          - 如果内部有典型公式字符 => 去掉两侧 $
          - 否则 (纯数字/货币等) => 保留 "$...$"
        '''
        content = m.group(1)
        # 判断内容是否包含典型公式字符
        if any(c in MarkdownCleaner._formula_chars for c in content):
            return content
        return m.group(0)

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        '''
        当匹配到一个整段表格块时，回调该函数。
        '''
        table = match.group(0)
        # 只保留表格内容，去除多余空行
        lines = [line.strip()
                 for line in table.strip().split('\n') if line.strip()]
        return '\n'.join(lines)

    @staticmethod
    def clean_markdown(text: str) -> str:
        '''
        主入口方法：依序执行所有正则，移除或替换 Markdown 元素
        '''
        # 1. 移除代码块

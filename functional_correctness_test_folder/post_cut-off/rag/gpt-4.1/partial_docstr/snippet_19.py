import re


class MarkdownCleaner:
    '''
    封装 Markdown 清理逻辑：直接用 MarkdownCleaner.clean_markdown(text) 即可
    '''
    # 典型公式字符集合
    _formula_chars = set(
        '=^_\\{}[]|<>/()*+-√αβγδεζηθικλμνξοπρστυφχψω∞∑∏∫∂∇∈∉∪∩∅∃∀→←⇔≠≈≥≤±·…！!@#￥%&')

    @staticmethod
    def _replace_inline_dollar(m: re.Match) -> str:
        '''
        只要捕获到完整的 "$...$":
          - 如果内部有典型公式字符 => 去掉两侧 $
          - 否则 (纯数字/货币等) => 保留 "$...$"
        '''
        inner = m.group(1)
        # 判断是否包含典型公式字符
        if any(c in MarkdownCleaner._formula_chars for c in inner):
            return inner
        # 允许空格、数字、字母、逗号、点、美元符号等
        if re.fullmatch(r'[\d\w\s,.\-:/$¥€£]+', inner):
            return m.group(0)
        return inner

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        '''
        当匹配到一个整段表格块时，回调该函数。
        '''
        table = match.group(0)
        # 去除表格两侧的空行
        table = table.strip('\n')
        # 将表格用空行包裹，便于后续处理
        return '\n' + table + '\n'

    @staticmethod
    def clean_markdown(text: str) -> str:
        '''
        主入口方法：依序执行所有正则，移除或替换 Markdown 元素
        '''
        # 1. 移除代码块 ```...```
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        # 2. 移除行内代码 `...`
        text = re.sub(r'`([^`]+)`', r'\1', text)
        # 3. 处理表格块

        def table_block_replacer(m):
            return MarkdownCleaner._replace_table_block(m)
        text = re.sub(
            r'(?:^|\n)((?:\|[^\n]*\|\n)+)',
            table_block_replacer,
            text,
            flags=re.MULTILINE
        )
        # 4. 处理 $...$ 行内公式
        text = re.sub(
            r'\$([^\$]+)\$',
            MarkdownCleaner._replace_inline_dollar,
            text
        )
        # 5. 移除图片 ![alt](url)
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
        # 6. 移除链接 [text](url) -> text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        # 7. 移除标题
        text = re.sub(r'^\s{0,3}#{1,6}\s*', '', text, flags=re.MULTILINE)
        # 8. 移除无序列表符号
        text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
        # 9. 移除有序列表符号
        text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
        # 10. 移除引用符号
        text = re.sub(r'^\s*>+\s*', '', text, flags=re.MULTILINE)
        # 11. 移除粗体/斜体
        text = re.sub(r'(\*\*|__)(.*?)\1', r'\2', text)
        text = re.sub(r'(\*|_)(.*?)\1', r'\2', text)
        # 12. 移除多余的空行
        text = re.sub(r'\n{3,}', '\n\n', text)
        # 13. 去除行首尾空格
        text = '\n'.join(line.strip() for line in text.splitlines())
        # 14. 再次去除多余空行
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

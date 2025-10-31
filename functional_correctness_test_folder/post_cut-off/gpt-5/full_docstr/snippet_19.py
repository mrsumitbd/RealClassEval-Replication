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
        inner = m.group(1).strip()
        if not inner:
            return m.group(0)
        # 判断是否为公式：典型 LaTeX 符号 或 命令
        if re.search(r'(\\[A-Za-z]+|[\\^_{}=])', inner):
            return inner
        return m.group(0)

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        '''
        当匹配到一个整段表格块时，回调该函数。
        '''
        block = match.group(0)
        lines = block.strip('\n').split('\n')
        out_lines = []
        align_re = re.compile(r'^\s*\|?(?:\s*:?-+:?\s*\|)+\s*:?-+:?\s*\|?\s*$')
        for ln in lines:
            if align_re.match(ln):
                continue
            if '|' not in ln:
                continue
            row = [c.strip() for c in ln.strip().strip('|').split('|')]
            out_lines.append(' | '.join(row).strip())
        return '\n'.join(out_lines) + ('\n' if block.endswith('\n') else '')

    @staticmethod
    def clean_markdown(text: str) -> str:
        '''
        主入口方法：依序执行所有正则，移除或替换 Markdown 元素
        '''
        if not text:
            return ''

        s = text.replace('\r\n', '\n').replace('\r', '\n')

        # 表格：先处理表格块，避免后续对竖线的破坏
        table_pat = re.compile(
            r'(?ms)^(?:[^\n]*\|[^\n]*\n)+^\s*\|?(?:\s*:?-+:?\s*\|)+\s*:?-+:?\s*\|?\s*$\n?(?:[^\n]*\|[^\n]*\n?)*'
        )
        s = table_pat.sub(MarkdownCleaner._replace_table_block, s)

        # 代码块 ```...``` -> 保留内容，移除围栏
        s = re.sub(r'(?ms)```[^\n]*\n(.*?)```', lambda m: m.group(1), s)
        # 单行围栏（非标准但常见）
        s = re.sub(r'(?m)^```+\s*$', '', s)

        # 行内代码 `code` -> code
        s = re.sub(r'`([^`]+)`', r'\1', s)

        # 图片 ![alt](url) -> alt
        s = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', s)

        # 链接 [text](url) -> text
        s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)

        # 标题 # ... -> 文本
        s = re.sub(r'(?m)^\s{0,3}#{1,6}\s*', '', s)

        # 引用 > -> 去掉前缀
        s = re.sub(r'(?m)^\s{0,3}>\s?', '', s)

        # 粗体/斜体/删除线
        s = re.sub(r'(\*\*|__)(.*?)\1', r'\2', s)  # 粗体
        s = re.sub(r'~~(.*?)~~', r'\1', s)        # 删除线
        # 斜体（在粗体之后，避免与粗体冲突）
        s = re.sub(r'(?<!\*)\*(?!\*)([^*\n]+)(?<!\*)\*(?!\*)', r'\1', s)
        s = re.sub(r'(?<!_)_(?!_)([^_\n]+)(?<!_)_(?!_)', r'\1', s)

        # 水平分割线 -> 空行
        s = re.sub(r'(?m)^\s*(?:-{3,}|\*{3,}|_{3,})\s*$', '', s)

        # 列表前缀
        s = re.sub(r'(?m)^\s{0,3}(?:[-+*]\s+)', '', s)       # 无序列表
        s = re.sub(r'(?m)^\s{0,3}\d+\.\s+', '', s)           # 有序列表

        # 行内美元公式：只去掉 $...$ 外壳（非 $$...$$）
        inline_dollar_pat = re.compile(r'(?<!\$)\$([^$\n]+?)\$(?!\$)')
        s = inline_dollar_pat.sub(MarkdownCleaner._replace_inline_dollar, s)

        # 去除剩余转义斜杠（只处理常见 Markdown 特殊字符前的反斜杠）
        s = re.sub(r'\\([\\`*_{}\[\]()#+.!-])', r'\1', s)

        # 合并多余空行，清理首尾空白
        s = re.sub(r'[ \t]+\n', '\n', s)
        s = re.sub(r'\n{3,}', '\n\n', s)
        return s.strip()

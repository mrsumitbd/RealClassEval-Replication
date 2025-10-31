import re
from typing import Optional


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
        inner = m.group(1)
        # 典型公式字符或字母，视为公式
        if re.search(r'[A-Za-z]', inner) or re.search(r'[\\{}_^=+\-*/<>()[\]]', inner):
            return inner
        return m.group(0)

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        '''
        当匹配到一个整段表格块时，回调该函数。
        '''
        block = match.group(0)
        lines = block.strip('\n').splitlines()
        if not lines:
            return ''
        align_re = re.compile(r'^\s*\|?(?:\s*:?-+:?\s*\|)+\s*:?-+:?\s*\|?\s*$')
        out_lines = []
        for ln in lines:
            s = ln.strip()
            if not s:
                continue
            if align_re.match(s):
                continue
            parts = [p.strip() for p in s.split('|')]
            if parts and parts[0] == '':
                parts = parts[1:]
            if parts and parts[-1] == '':
                parts = parts[:-1]
            if not parts:
                continue
            out_lines.append('  '.join(parts))
        return ('\n'.join(out_lines) + '\n') if out_lines else ''

    @staticmethod
    def clean_markdown(text: str) -> str:
        '''
        主入口方法：依序执行所有正则，移除或替换 Markdown 元素
        '''
        if not text:
            return ''
        s = text.replace('\r\n', '\n').replace('\r', '\n')

        # 移除/还原代码块围栏，仅保留代码内容
        s = re.sub(r'```[^\n]*\n(.*?)```',
                   lambda m: m.group(1), s, flags=re.DOTALL)
        s = re.sub(r'~~~[^\n]*\n(.*?)~~~',
                   lambda m: m.group(1), s, flags=re.DOTALL)

        # 内联代码
        s = re.sub(r'`([^`]+)`', r'\1', s)

        # 图片: ![alt](url) => alt
        s = re.sub(r'!\[([^\]]*)\]\((?:[^)]+)\)', r'\1', s)

        # 链接: [text](url) => text
        s = re.sub(r'\[([^\]]+)\]\((?:[^)]+)\)', r'\1', s)

        # 自动链接 <http://...> 或邮箱
        s = re.sub(r'<(https?://[^>\s]+)>', r'\1', s)
        s = re.sub(
            r'<([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})>', r'\1', s)

        # 标题前缀
        s = re.sub(r'^\s{0,3}#{1,6}\s*', '', s, flags=re.MULTILINE)

        # 引用块 '>'
        s = re.sub(r'^\s{0,3}>\s?', '', s, flags=re.MULTILINE)

        # 水平分割线
        s = re.sub(r'^\s*([-*_])(?:\s*\1){2,}\s*$', '', s, flags=re.MULTILINE)

        # 列表项前缀与任务列表复选框
        s = re.sub(r'^\s*[-*+]\s+\[[ xX]\]\s*', '', s, flags=re.MULTILINE)
        s = re.sub(r'^\s*[-*+]\s+', '', s, flags=re.MULTILINE)
        s = re.sub(r'^\s*\d+[.)]\s+', '', s, flags=re.MULTILINE)

        # 删除线、粗体、斜体
        s = re.sub(r'~~(.*?)~~', r'\1', s)
        s = re.sub(r'(\*\*|__)(.*?)\1', r'\2', s, flags=re.DOTALL)
        s = re.sub(r'(\*|_)(.*?)\1', r'\2', s, flags=re.DOTALL)

        # 表格块：将表格转为普通文本，忽略对齐分隔行
        table_block_re = re.compile(
            r'(?:^\s*\|[^\n]*\n){2,}', flags=re.MULTILINE)
        s = table_block_re.sub(MarkdownCleaner._replace_table_block, s)

        # 展示公式 $$...$$ => 去除 $$
        s = re.sub(r'\$\$(.*?)\$\$', r'\1', s, flags=re.DOTALL)

        # 内联公式 $...$ => 根据规则决定是否去掉 $
        inline_dollar_re = re.compile(
            r'(?<!\\)(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)')
        s = inline_dollar_re.sub(MarkdownCleaner._replace_inline_dollar, s)

        # 反斜杠转义
        s = re.sub(r'\\([\\`*_{}\[\]()#+\-.!|>~])', r'\1', s)

        # 去掉行尾多余空白
        s = re.sub(r'[ \t]+$', '', s, flags=re.MULTILINE)

        # 合并多余空行为最多两个
        s = re.sub(r'\n{3,}', '\n\n', s)

        return s.strip()

import re
from typing import Match


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
        # 典型的公式特征：有 LaTeX 命令、上/下标、花括号等
        if re.search(r'(\\[a-zA-Z]+|[\\^_{}])', content):
            return content
        return m.group(0)

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        '''
        当匹配到一个整段表格块时，回调该函数。
        '''
        block = match.group(0).strip('\n')
        lines = [ln.rstrip() for ln in block.splitlines() if ln.strip()]
        if not lines:
            return ''
        # 忽略分隔行（---|:---:|--- 等）
        sep_re = re.compile(
            r'^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$')
        cleaned_rows = []
        for ln in lines:
            if sep_re.match(ln):
                continue
            # 去除两端竖线后拆分单元格
            row = [c.strip() for c in ln.strip().strip('|').split('|')]
            row = [c for c in row if c]  # 去除空单元格
            if row:
                cleaned_rows.append('  '.join(row))
        return ('\n'.join(cleaned_rows) + '\n') if cleaned_rows else ''

    @staticmethod
    def clean_markdown(text: str) -> str:
        '''
        主入口方法：依序执行所有正则，移除或替换 Markdown 元素
        '''
        if not text:
            return ''

        s = text.replace('\r\n', '\n').replace('\r', '\n')

        # 移除 HTML 注释
        s = re.sub(r'<!--.*?-->', '', s, flags=re.DOTALL)

        # 处理代码块 (``` 或 ~~~) - 保留内容，去掉围栏
        s = re.sub(r'```[ \t]*[a-zA-Z0-9_-]*\n?(.*?)(?:```)',
                   r'\1', s, flags=re.DOTALL)
        s = re.sub(r'~~~[ \t]*[a-zA-Z0-9_-]*\n?(.*?)(?:~~~)',
                   r'\1', s, flags=re.DOTALL)

        # 行内代码：`code` -> code
        s = re.sub(r'`([^`]+)`', r'\1', s)

        # 标题前缀：# ## ... -> 去掉 # 与紧随空格
        s = re.sub(r'^\s{0,3}#{1,6}\s*', '', s, flags=re.MULTILINE)

        # 引用块：> -> 去掉
        s = re.sub(r'^\s{0,3}>\s?', '', s, flags=re.MULTILINE)

        # 任务列表标记
        s = re.sub(r'^\s{0,3}[-+*]\s+\[(?: |x|X)\]\s+',
                   '', s, flags=re.MULTILINE)

        # 无序列表标记
        s = re.sub(r'^\s{0,3}[-+*]\s+', '', s, flags=re.MULTILINE)

        # 有序列表标记
        s = re.sub(r'^\s{0,3}\d+[.)]\s+', '', s, flags=re.MULTILINE)

        # 水平分割线
        s = re.sub(r'^\s{0,3}(?:[-*_]\s*){3,}\s*$', '', s, flags=re.MULTILINE)

        # 图片：![alt](url) -> alt
        s = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'\1', s)
        s = re.sub(r'!\[([^\]]*)\]\[[^\]]*\]', r'\1', s)

        # 链接：[text](url) -> text；[text][id] -> text；行内链接定义移除
        s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', s)
        s = re.sub(r'\[([^\]]+)\]\[[^\]]*\]', r'\1', s)
        s = re.sub(r'^\s*\[[^\]]+\]:\s+\S+.*$', '', s, flags=re.MULTILINE)

        # 删除删除线：~~text~~ -> text
        s = re.sub(r'~~(.*?)~~', r'\1', s)

        # 加粗与斜体：**text**、__text__、*text*、_text_ -> text
        s = re.sub(r'(\*\*|__)(.*?)\1', r'\2', s, flags=re.DOTALL)
        s = re.sub(r'(\*|_)(.*?)\1', r'\2', s, flags=re.DOTALL)

        # 数学块：$$...$$ -> 提取内容
        s = re.sub(r'\$\$(.+?)\$\$', r'\1', s, flags=re.DOTALL)

        # 表格块：将表格转为简单文本
        table_block_re = re.compile(
            r'(^[ \t]*\|.*\n'                       # 表头
            r'[ \t]*\|?\s*:?-{3,}:?(?:\s*\|\s*:?-{3,}:?)+\s*\|?[ \t]*\n'  # 分隔行
            r'(?:[ \t]*\|.*(?:\n|$))+)',            # 数据行
            flags=re.MULTILINE
        )
        s = table_block_re.sub(MarkdownCleaner._replace_table_block, s)

        # 行内 $...$ 数学：根据内容判断是否去掉 $
        inline_dollar_re = re.compile(
            r'(?<!\\)(?<!\$)\$(?!\$)(.+?)(?<!\$)(?<!\\)\$(?!\$)')
        s = inline_dollar_re.sub(MarkdownCleaner._replace_inline_dollar, s)

        # 去除残余的多余转义符（常见对 Markdown 的转义）
        s = s.replace('\\*', '*').replace('\\_', '_').replace('\\#',
                                                              '#').replace('\\`', '`').replace('\\|', '|').replace('\\-', '-')

        # 清理每行末尾空白
        s = re.sub(r'[ \t]+$', '', s, flags=re.MULTILINE)

        # 合并多余的空行为最多两行
        s = re.sub(r'\n{3,}', '\n\n', s)

        return s.strip()

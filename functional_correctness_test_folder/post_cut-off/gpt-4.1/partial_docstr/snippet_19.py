
import re


class MarkdownCleaner:

    @staticmethod
    def _replace_inline_dollar(m: re.Match) -> str:
        '''
        只要捕获到完整的 "$...$":
          - 如果内部有典型公式字符 => 去掉两侧 $
          - 否则 (纯数字/货币等) => 保留 "$...$"
        '''
        content = m.group(1)
        # 典型公式字符: 字母、下划线、反斜杠、^、_、{、}、\frac、\sum、\int、\lim、\infty、\cdots、\leq、\geq、\neq、\approx、\sin、\cos、\tan、\log、\exp、\sqrt
        # 只要有字母或下划线或反斜杠或 ^ _ { }，就认为是公式
        if re.search(r'[a-zA-Z_\\^{}]', content):
            return content
        return m.group(0)

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        # 只保留表格内容，去掉 markdown 表格的 | 和 --- 等
        table = match.group(0)
        lines = table.strip().split('\n')
        # 跳过第二行 (分隔符)
        if len(lines) >= 2 and re.match(r'^\s*\|?[\s:-]+\|?[\s:-]*$', lines[1]):
            header = lines[0]
            rows = lines[2:]
        else:
            header = lines[0]
            rows = lines[1:]
        # 处理每一行，去掉首尾 |，并用制表符分隔

        def clean_line(line):
            line = line.strip()
            if line.startswith('|'):
                line = line[1:]
            if line.endswith('|'):
                line = line[:-1]
            return '\t'.join([cell.strip() for cell in line.split('|')])
        cleaned = [clean_line(header)] + [clean_line(row)
                                          for row in rows if row.strip()]
        return '\n'.join(cleaned)

    @staticmethod
    def clean_markdown(text: str) -> str:
        '''
        主入口方法：依序执行所有正则，移除或替换 Markdown 元素
        '''
        # 1. 处理表格
        # 匹配 markdown 表格块
        table_pattern = re.compile(
            r'(?:^\s*\|.*\|\s*\n'      # header
            r'^\s*\|?[\s:-]+\|?[\s:-]*\n'  # separator
            r'(?:^\s*\|.*\|\s*\n?)+)',     # rows
            re.MULTILINE)
        text = table_pattern.sub(MarkdownCleaner._replace_table_block, text)

        # 2. 处理 $...$ 行内公式
        text = re.sub(
            r'\$(.+?)\$', MarkdownCleaner._replace_inline_dollar, text)

        # 3. 移除代码块

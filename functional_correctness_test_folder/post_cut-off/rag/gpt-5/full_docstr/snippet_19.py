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
        inner = m.group(1)
        # 典型 LaTeX/公式特征：反斜杠命令、上下标、花括号、等号、常见运算符等
        if re.search(r'(\\[a-zA-Z]+|[_^{}=]|[+\-*/<>]|\\\(|\\\))', inner):
            return inner
        return m.group(0)

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        '''
        当匹配到一个整段表格块时，回调该函数。
        '''
        block = match.group(0)
        lines = [ln.strip()
                 for ln in block.strip('\n').splitlines() if ln.strip()]
        # 表头分隔线匹配，如: | --- | :---: | ---: |
        sep_re = re.compile(r'^\|?\s*:?-{3,}:?(?:\s*\|\s*:?-{3,}:?)+\s*\|?$')

        cleaned = []
        for ln in lines:
            if sep_re.match(ln):
                continue
            # 去掉行首尾的竖线，再按竖线切分，去空白
            if '|' in ln:
                content = ln.strip('|').split('|')
                cells = [c.strip() for c in content]
                cleaned.append(' | '.join(cells))
            else:
                cleaned.append(ln)
        return '\n'.join(cleaned) + '\n'

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

        # 展开围栏代码块，保留内容
        s = re.sub(r'```[^\n]*\n([\s\S]*?)```', r'\1', s)
        s = re.sub(r'~~~[^\n]*\n([\s\S]*?)~~~', r'\1', s)

        # 处理表格块（仅处理以 | 开头的标准表格）
        table_block_re = re.compile(
            r'(?mx)'
            r'(?:^|\n)'                      # 前导行边界
            r'('
            r'^\s*\|.*\n'                    # 表头行（以 | 开头）
            r'^\s*\|?\s*:?-{3,}:?(?:\s*\|\s*:?-{3,}:?)+\s*\|?\s*$\n'  # 分隔线
            r'(?:^\s*\|.*\n)+'               # 至少一行数据
            r')'
        )
        s = table_block_re.sub(
            lambda m: '\n' + MarkdownCleaner._replace_table_block(m), s)

        # ATX 标题：# 标记去掉
        s = re.sub(r'(?m)^\s{0,3}#{1,6}\s*', '', s)
        # ATX 标题可能的结尾 # 去掉
        s = re.sub(r'(?m)\s+#{1,}\s*$', '', s)

        # Setext 标题分隔线移除
        s = re.sub(r'(?m)^\s*(=|-){3,}\s*$', '', s)

        # 水平分割线移除
        s = re.sub(r'(?m)^\s{0,3}([-*_]\s*){3,}\s*$', '', s)

        # 引用前缀去掉
        s = re.sub(r'(?m)^\s{0,3}>\s?', '', s)

        # 任务列表复选框标记去掉
        s = re.sub(r'(?m)^\s*[-+*]\s+\[(?: |x|X)\]\s+', '', s)

        # 无序列表/有序列表标记去掉（保留文本）
        s = re.sub(r'(?m)^\s*[-+*]\s+', '', s)
        s = re.sub(r'(?m)^\s*\d{1,3}[.)]\s+', '', s)

        # 图片：保留 alt 文本
        s = re.sub(r'!\[([^\]]*)\]\((?:[^)]+)\)', r'\1', s)

        # 链接：保留可见文本
        s = re.sub(r'\[([^\]]+)\]\((?:[^)]+)\)', r'\1', s)
        # 自动链接去掉尖括号
        s = re.sub(r'<(https?://[^ >]+)>', r'\1', s)
        s = re.sub(r'<mailto:([^ >]+)>', r'\1', s)

        # 行内代码：去掉反引号
        s = re.sub(r'`([^`]+)`', r'\1', s)

        # 强调/加粗/删除线：保留文本
        s = re.sub(r'\*\*(.+?)\*\*', r'\1', s)
        s = re.sub(r'__(.+?)__', r'\1', s)
        s = re.sub(r'(?<!\*)\*(.+?)\*(?!\*)', r'\1', s)
        s = re.sub(r'(?<!_)_(.+?)_(?!_)', r'\1', s)
        s = re.sub(r'~~(.+?)~~', r'\1', s)

        # 脚注引用与定义去掉
        s = re.sub(r'\[\^[^\]]+\]', '', s)                     # 引用
        s = re.sub(r'(?m)^\[\^[^\]]+\]:\s.*$', '', s)          # 定义

        # 处理行内 $...$：根据内容判断是否去掉美元符号
        inline_dollar_re = re.compile(r'(?<!\\)\$(?!\$)(.+?)(?<!\\)\$(?!\$)')
        s = inline_dollar_re.sub(MarkdownCleaner._replace_inline_dollar, s)

        # 解开常见的转义
        s = re.sub(r'\\([\\`*_{}\[\]()#+\-.!|>])', r'\1', s)

        # 移除残余 HTML 标签（可选）
        s = re.sub(r'</?[A-Za-z][^>]*>', '', s)

        # 去掉行尾空白
        s = re.sub(r'[ \t]+$', '', s, flags=re.MULTILINE)

        # 合并多余空行为最多一个
        s = re.sub(r'\n{3,}', '\n\n', s)

        return s.strip()

import re


class MarkdownCleaner:
    '''
    封装 Markdown 清理逻辑：直接用 MarkdownCleaner.clean_markdown(text) 即可
    '''
    # 典型公式字符集合
    _formula_chars = set('=+\\^_{}[]|<>/()*·αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ∞∑∏∫√∂∇≠≈≤≥→←↔⇔∈∉∪∩⊂⊃⊆⊇⊄⊅⊈⊉⊕⊗⊥∥∠∡∢∣∤∧∨¬∀∃∅∴∵∶∷∽≅≡⊿⊙⊚⊛⊝⊞⊟⊠⊡⊢⊣⊤⊥⊦⊧⊨⊩⊪⊫⊬⊭⊮⊯⊰⊱⊲⊳⊴⊵⊶⊷⊸⊹⊺⊻⊼⊽⊾⊿⌀⌅⌆⌈⌉⌊⌋⌌⌍⌎⌏⎯⎰⎱⎲⎳⏜⏝⏞⏟⏠⏡⏢⏣⏤⏥⏦⏧⏨⏩⏪⏫⏬⏭⏮⏯⏰⏱⏲⏳⏴⏵⏶⏷⏸⏹⏺⏻⏼⏽⏾⏿␀␁␂␃␄␅␆␇␈␉␊␋␌␍␎␏␐␑␒␓␔␕␖␗␘␙␚␛␜␝␞␟␠␡␢␣␤␥␦␧␨␩␪␫␬␭␮␯␰␱␲␳␴␵␶␷␸␹␺␻␼␽␾␿')
    _formula_pattern = re.compile(
        r'[\=\+\^_\\\{\}\[\]\|<>/()*·α-ωΑ-Ω∞∑∏∫√∂∇≠≈≤≥→←↔⇔∈∉∪∩⊂⊃⊆⊇⊄⊅⊈⊉⊕⊗⊥∥∠∡∢∣∤∧∨¬∀∃∅∴∵∶∷∽≅≡⊿⊙⊚⊛⊝⊞⊟⊠⊡⊢⊣⊤⊥⊦⊧⊨⊩⊪⊫⊬⊭⊮⊯⊰⊱⊲⊳⊴⊵⊶⊷⊸⊹⊺⊻⊼⊽⊾⊿⌀⌅⌆⌈⌉⌊⌋⌌⌍⌎⌏⎯⎰⎱⎲⎳⏜⏝⏞⏟⏠⏡⏢⏣⏤⏥⏦⏧⏨⏩⏪⏫⏬⏭⏮⏯⏰⏱⏲⏳⏴⏵⏶⏷⏸⏹⏺⏻⏼⏽⏾⏿]')

    @staticmethod
    def _replace_inline_dollar(m: re.Match) -> str:
        '''
        只要捕获到完整的 "$...$":
          - 如果内部有典型公式字符 => 去掉两侧 $
          - 否则 (纯数字/货币等) => 保留 "$...$"
        '''
        inner = m.group(1)
        if MarkdownCleaner._formula_pattern.search(inner):
            return inner
        return m.group(0)

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        '''
        当匹配到一个整段表格块时，回调该函数。
        '''
        table = match.group(0)
        # 只保留表格内容，去掉 markdown 的 | 和 --- 等
        lines = table.strip().splitlines()
        clean_lines = []
        for line in lines:
            # 跳过分隔线
            if re.match(r'^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$', line):
                continue
            # 去掉行首行尾的 |，并用制表符分隔
            line = line.strip()
            if line.startswith('|'):
                line = line[1:]
            if line.endswith('|'):
                line = line[:-1]
            clean_lines.append('\t'.join([cell.strip()
                               for cell in line.split('|')]))
        return '\n'.join(clean_lines)

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
        table_block_pattern = re.compile(
            r'(?:^\s*\|.*\|\s*$\n?)+', re.MULTILINE
        )
        text = table_block_pattern.sub(
            MarkdownCleaner._replace_table_block, text)
        # 4. 处理 $...$ 行内公式
        text = re.sub(
            r'\$(.+?)\$', MarkdownCleaner._replace_inline_dollar, text)
        # 5. 移除图片 ![alt](url)
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
        # 6. 移除链接 [text](url) -> text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        # 7. 移除标题 #/##/### 等
        text = re.sub(r'^\s{0,3}#{1,6}\s*', '', text, flags=re.MULTILINE)
        # 8. 移除无序/有序列表标记
        text = re.sub(r'^\s*([-*+]|\d+\.)\s+', '', text, flags=re.MULTILINE)
        # 9. 移除引用 >
        text = re.sub(r'^\s*>\s?', '', text, flags=re.MULTILINE)
        # 10. 移除粗体/斜体 **text** *text* __text__ _text_
        text = re.sub(r'(\*\*|__)(.*?)\1', r'\2', text)
        text = re.sub(r'(\*|_)(.*?)\1', r'\2', text)
        # 11. 移除多余空行
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

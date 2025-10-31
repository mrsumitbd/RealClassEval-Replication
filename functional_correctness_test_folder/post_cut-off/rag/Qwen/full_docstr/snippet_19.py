
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
        if re.search(r'[a-zA-Z]', content):
            return content
        return m.group(0)

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        '''
        当匹配到一个整段表格块时，回调该函数。
        '''
        return ''

    @staticmethod
    def clean_markdown(text: str) -> str:
        '''
        主入口方法：依序执行所有正则，移除或替换 Markdown 元素
        '''
        # Remove or replace inline dollar signs
        text = re.sub(
            r'\$(.*?)\$', MarkdownCleaner._replace_inline_dollar, text)

        # Remove table blocks
        text = re.sub(r'\|.*?\|\n(\|.*?\|\n)+',
                      MarkdownCleaner._replace_table_block, text, flags=re.DOTALL)

        # Remove headers
        text = re.sub(r'#{1,6}\s+.*', '', text)

        # Remove emphasis (bold and italic)
        text = re.sub(r'\*\*|__', '', text)
        text = re.sub(r'\*|_', '', text)

        # Remove links
        text = re.sub(r'\[.*?\]\(.*?\)', '', text)

        # Remove images
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)

        # Remove blockquotes
        text = re.sub(r'>\s*.*', '', text)

        # Remove lists
        text = re.sub(r'^\s*[-+*]\s+.*', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*\d+\.\s+.*', '', text, flags=re.MULTILINE)

        # Remove code blocks
        text = re.sub(r'

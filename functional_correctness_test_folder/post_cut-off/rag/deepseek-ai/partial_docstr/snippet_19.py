
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
        if any(c in content for c in ['=', '+', '-', '*', '/', '^', '_', '(', ')']):
            return content
        return f'${content}$'

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
        # 处理行内公式的 $
        text = re.sub(
            r'\$(.+?)\$', MarkdownCleaner._replace_inline_dollar, text)

        # 移除表格
        table_pattern = r'(\|.+\|[\r\n]+)((?:\|.*\|[\r\n]+)+)'
        text = re.sub(
            table_pattern, MarkdownCleaner._replace_table_block, text)

        # 移除图片
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)

        # 移除链接
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)

        # 移除粗体/斜体标记
        text = re.sub(r'(\*\*|__)(.*?)\1', r'\2', text)
        text = re.sub(r'(\*|_)(.*?)\1', r'\2', text)

        # 移除代码块
        text = re.sub(r'

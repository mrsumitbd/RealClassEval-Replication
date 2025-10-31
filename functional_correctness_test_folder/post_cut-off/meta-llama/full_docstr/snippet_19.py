
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
        if any(char in content for char in '^_~\\{}'):
            return content
        if re.search(r'[+\-*/=<>]', content):
            return content
        return m.group(0)

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        '''
        当匹配到一个整段表格块时，回调该函数。
        '''
        return '\n'

    @staticmethod
    def clean_markdown(text: str) -> str:
        '''
        主入口方法：依序执行所有正则，移除或替换 Markdown 元素
        '''
        # 行内公式： "$...$" -> "..."
        text = re.sub(r'\$([^$\n]+?)\$',
                      MarkdownCleaner._replace_inline_dollar, text)

        # 删除图片： ![alt](url) -> ""
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)

        # 删除链接： [text](url) -> "text"
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)

        # 删除表格块
        text = re.sub(
            r'(^\|.*\|$\n?)+', MarkdownCleaner._replace_table_block, text, flags=re.MULTILINE)

        # 删除标题： # xxxx -> "xxxx"
        text = re.sub(r'^#{1,6} ', '', text, flags=re.MULTILINE)

        # 删除粗体、斜体： **xxx** -> "xxx", *xxx* -> "xxx"
        text = re.sub(r'\*{1,2}(.*?)\*{1,2}', r'\1', text)

        # 删除删除线： ~~xxx~~ -> "xxx"
        text = re.sub(r'~~(.*?)~~', r'\1', text)

        # 删除行内代码： `xxx` -> "xxx"
        text = re.sub(r'`(.*?)`', r'\1', text)

        # 删除代码块：

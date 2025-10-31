
import re


class HtmlUtil:
    """
    This is a class as util for html, supporting for formatting and extracting code from HTML text, including cleaning up the text and converting certain elements into specific marks.
    """

    def __init__(self):
        """
        Initialize a series of labels
        """
        self.SPACE_MARK = '-SPACE-'
        self.JSON_MARK = '-JSON-'
        self.MARKUP_LANGUAGE_MARK = '-MARKUP_LANGUAGE-'
        self.URL_MARK = '-URL-'
        self.NUMBER_MARK = '-NUMBER-'
        self.TRACE_MARK = '-TRACE-'
        self.COMMAND_MARK = '-COMMAND-'
        self.COMMENT_MARK = '-COMMENT-'
        self.CODE_MARK = '-CODE-'

    @staticmethod
    def __format_line_feed(text):
        """
        Replace consecutive line breaks with a single line break
        :param text: string with consecutive line breaks
        :return:string, replaced text with single line break
        """
        # Normalize line endings
        text = re.sub(r'\r\n|\r', '\n', text)
        # Collapse multiple newlines into one
        text = re.sub(r'\n+', '\n', text)
        return text

    def format_line_html_text(self, html_text):
        """
        get the html text without the code, and add the code tag -CODE- where the code is
        :param html_text:string
        :return:string
        >>>htmlutil = HtmlUtil()
        >>>htmlutil.format_line_html_text('<html>\n<body>\n   <h1>Title</h1>\n   <p>This is a paragraph.</p>\n   <pre>print(\'Hello, world!\')</pre>\n   <p>Another paragraph.</p>\n   <pre><code>for i in range(5):\n   print(i)</code></pre>\n</body>\n</html>')
        'Title\nThis is a paragraph.\n-CODE-\nAnother paragraph.\n-CODE-'
        """
        # Replace code blocks with marker
        code_pattern = re.compile(
            r'<pre[^>]*>(?:<code[^>]*>)?(.*?)</code>?</pre>', re.DOTALL | re.IGNORECASE)
        replaced = code_pattern.sub('\n' + self.CODE_MARK + '\n', html_text)

        # Remove all remaining tags
        text_without_tags = re.sub(r'<[^>]+>', '', replaced)

        # Collapse line breaks and strip whitespace
        cleaned = self.__format_line_feed(text_without_tags).strip()

        # Remove leading/trailing spaces on each line
        cleaned_lines = [line.strip() for line in cleaned.split('\n')]
        return '\n'.join(cleaned_lines)

    def extract_code_from_html_text(self, html_text):
        """
        extract codes from the html body
        :param html_text: string, html text
        :return: the list of code
        >>>htmlutil = HtmlUtil()
        >>>htmlutil.extract_code_from_html_text('<html>\n<body>\n   <h1>Title</h1>\n   <p>This is a paragraph.</p>\n   <pre>print(\'Hello, world!\')</pre>\n   <p>Another paragraph.</p>\n   <pre><code>for i in range(5):\n   print(i)</code></pre>\n</body>\n</html>')
        ["print('Hello, world!')", 'for i in range(5):\\n   print(i)']
        """
        code_pattern = re.compile(
            r'<pre[^>]*>(?:<code[^>]*>)?(.*?)</code>?</pre>', re.DOTALL | re.IGNORECASE)
        matches = code_pattern.findall(html_text)
        # Strip leading/trailing whitespace from each code block
        return [match.strip() for match in matches]

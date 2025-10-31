import re
import html


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
        if text is None:
            return ''
        # Normalize newlines
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        # Collapse runs of blank lines to a single newline
        text = re.sub(r'\n\s*\n+', '\n', text)
        return text

    def format_line_html_text(self, html_text):
        """
        get the html text without the code, and add the code tag -CODE- where the code is
        :param html_text:string
        :return:string
        >>>htmlutil = HtmlUtil()
        >>>htmlutil.format_line_html_text(<html>
        >>> <body>
        >>>    <h1>Title</h1>
        >>>    <p>This is a paragraph.</p>
        >>>    <pre>print('Hello, world!')</pre>
        >>>    <p>Another paragraph.</p>
        >>>    <pre><code>for i in range(5):
        >>>    print(i)</code></pre>
        >>>    </body>
        >>>    </html>)
        Title
        This is a paragraph.
        -CODE-
        Another paragraph.
        -CODE-
        """
        if not isinstance(html_text, str):
            return ''
        # Extract body if present
        body_match = re.search(
            r'<body[^>]*>(.*?)</body\s*>', html_text, flags=re.IGNORECASE | re.DOTALL)
        text = body_match.group(1) if body_match else html_text

        # Remove script and style contents entirely
        text = re.sub(r'<script[^>]*>.*?</script\s*>',
                      '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style\s*>', '',
                      text, flags=re.IGNORECASE | re.DOTALL)

        # Replace <pre>...</pre> with marker on its own line
        def _pre_replacer(match):
            return '\n' + self.CODE_MARK + '\n'

        text = re.sub(r'<pre\b[^>]*>.*?</pre\s*>', _pre_replacer,
                      text, flags=re.IGNORECASE | re.DOTALL)

        # Convert some block/line-break tags to newlines to preserve structure
        # br variants
        text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
        # Closing block tags that should end a line
        block_closers = ['p', 'div', 'section', 'article', 'header', 'footer', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                         'li', 'ul', 'ol', 'table', 'tr', 'td', 'th', 'blockquote']
        for tag in block_closers:
            text = re.sub(rf'</{tag}\s*>', '\n', text, flags=re.IGNORECASE)

        # Strip remaining tags
        text = re.sub(r'<[^>]+>', '', text)

        # Unescape HTML entities
        text = html.unescape(text)

        # Normalize whitespace lines: trim and remove empty lines
        text = self.__format_line_feed(text)
        lines = [ln.strip() for ln in text.split('\n')]
        lines = [ln for ln in lines if ln != '']
        # Collapse consecutive -CODE- lines (in case)
        result_lines = []
        prev_code = False
        for ln in lines:
            if ln == self.CODE_MARK:
                if not prev_code:
                    result_lines.append(ln)
                prev_code = True
            else:
                result_lines.append(ln)
                prev_code = False

        return '\n'.join(result_lines)

    def extract_code_from_html_text(self, html_text):
        """
        extract codes from the html body
        :param html_text: string, html text
        :return: the list of code
        >>>htmlutil = HtmlUtil()
        >>>htmlutil.extract_code_from_html_text(<html>
        >>> <body>
        >>>    <h1>Title</h1>
        >>>    <p>This is a paragraph.</p>
        >>>    <pre>print('Hello, world!')</pre>
        >>>    <p>Another paragraph.</p>
        >>>    <pre><code>for i in range(5):
        >>>    print(i)</code></pre>
        >>>    </body>
        >>>    </html>)
        ["print('Hello, world!')", 'for i in range(5):\n                print(i)']
        """
        if not isinstance(html_text, str):
            return []
        # Extract body if present
        body_match = re.search(
            r'<body[^>]*>(.*?)</body\s*>', html_text, flags=re.IGNORECASE | re.DOTALL)
        text = body_match.group(1) if body_match else html_text

        # Find all <pre> blocks
        codes = []
        for m in re.finditer(r'<pre\b[^>]*>(.*?)</pre\s*>', text, flags=re.IGNORECASE | re.DOTALL):
            inner = m.group(1)
            # Remove HTML tags inside (e.g., <code>, span for highlighting)
            inner_no_tags = re.sub(r'<[^>]+>', '', inner, flags=re.DOTALL)
            # Unescape entities to get raw code
            inner_unescaped = html.unescape(inner_no_tags)
            # Normalize newlines and strip leading/trailing whitespace
            code = inner_unescaped.replace(
                '\r\n', '\n').replace('\r', '\n').strip()
            codes.append(code)
        return codes

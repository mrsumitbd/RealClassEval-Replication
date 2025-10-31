
import re
from html import unescape


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
        return re.sub(r'(\r?\n)+', '\n', text)

    def format_line_html_text(self, html_text):
        """
        get the html text without the code, and add the code tag -CODE- where the code is
        :param html_text:string
        :return:string
        """
        # Remove script and style
        html_text = re.sub(
            r'<(script|style)[^>]*>.*?</\1>', '', html_text, flags=re.DOTALL | re.IGNORECASE)
        # Find all <pre>...</pre> blocks (with or without <code> inside)
        code_blocks = []

        def code_replacer(match):
            code_blocks.append(match.group(0))
            return self.CODE_MARK

        # Replace <pre>...</pre> with -CODE-
        text_with_code_marks = re.sub(
            r'<pre\b[^>]*>.*?</pre>', code_replacer, html_text, flags=re.DOTALL | re.IGNORECASE)

        # Remove all HTML tags except -CODE-
        def tag_replacer(m):
            tag = m.group(0)
            if self.CODE_MARK in tag:
                return tag
            return ''

        text_no_tags = re.sub(r'<[^>]+>', tag_replacer, text_with_code_marks)
        # Unescape HTML entities
        text_no_tags = unescape(text_no_tags)
        # Remove leading/trailing whitespace on each line
        lines = [line.strip() for line in text_no_tags.splitlines()]
        # Remove empty lines
        lines = [line for line in lines if line]
        # Replace consecutive -CODE- marks with a single one
        result_lines = []
        prev_code = False
        for line in lines:
            if line == self.CODE_MARK:
                if not prev_code:
                    result_lines.append(line)
                prev_code = True
            else:
                result_lines.append(line)
                prev_code = False
        return '\n'.join(result_lines)

    def extract_code_from_html_text(self, html_text):
        """
        extract codes from the html body
        :param html_text: string, html text
        :return: the list of code
        """
        # Remove script and style
        html_text = re.sub(
            r'<(script|style)[^>]*>.*?</\1>', '', html_text, flags=re.DOTALL | re.IGNORECASE)
        # Find all <pre>...</pre> blocks
        code_blocks = re.findall(
            r'<pre\b[^>]*>(.*?)</pre>', html_text, flags=re.DOTALL | re.IGNORECASE)
        codes = []
        for block in code_blocks:
            # If <code>...</code> inside <pre>, extract only <code>
            code_inside = re.search(
                r'<code\b[^>]*>(.*?)</code>', block, flags=re.DOTALL | re.IGNORECASE)
            if code_inside:
                code = code_inside.group(1)
            else:
                code = block
            # Remove all HTML tags inside code
            code = re.sub(r'<[^>]+>', '', code)
            # Unescape HTML entities
            code = unescape(code)
            # Strip leading/trailing whitespace/newlines
            code = code.strip('\r\n')
            codes.append(code)
        return codes

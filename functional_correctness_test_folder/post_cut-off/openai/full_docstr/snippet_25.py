
import re
from typing import List
from urllib.parse import urlparse, unquote, urljoin


class URLExtractor:
    '''URL提取器'''

    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        """
        将arXiv网页链接转换为PDF下载链接

        支持的输入形式:
            https://arxiv.org/abs/xxxx.xxxx
            https://arxiv.org/abs/xxxx.xxxxv1
            https://arxiv.org/pdf/xxxx.xxxx.pdf
            https://arxiv.org/pdf/xxxx.xxxxv1.pdf
            https://arxiv.org/format/xxxx.xxxx.pdf
        输出形式:
            https://arxiv.org/pdf/xxxx.xxxx.pdf
        """
        if not url:
            return url

        parsed = urlparse(url)
        if parsed.netloc.lower() != "arxiv.org":
            return url

        path = parsed.path
        # 处理 /abs/ 形式
        abs_match = re.match(r"^/abs/([0-9]+\.[0-9]+(?:v[0-9]+)?)$", path)
        if abs_match:
            paper_id = abs_match.group(1)
            return f"https://arxiv.org/pdf/{paper_id}.pdf"

        # 处理 /pdf/ 形式，确保以 .pdf 结尾
        pdf_match = re.match(
            r"^/pdf/([0-9]+\.[0-9]+(?:v[0-9]+)?)(\.pdf)?$", path)
        if pdf_match:
            paper_id = pdf_match.group(1)
            return f"https://arxiv.org/pdf/{paper_id}.pdf"

        # 处理 /format/ 形式
        format_match = re.match(
            r"^/format/([0-9]+\.[0-9]+(?:v[0-9]+)?)(\.pdf)?$", path)
        if format_match:
            paper_id = format_match.group(1)
            return f"https://arxiv.org/pdf/{paper_id}.pdf"

        # 其它情况保持原样
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        """
        从文本中提取 URL

        支持 http, https, ftp, file 等协议
        """
        if not text:
            return []

        # 简单的 URL 正则，兼容常见情况
        url_pattern = re.compile(
            r"""
            (?P<url>
                (?:(?:https?|ftp|file)://)   # 协议
                [^\s<>"']+                   # 非空白、<>"' 的字符
            )
            """,
            re.VERBOSE | re.IGNORECASE,
        )

        urls = []
        for match in url_pattern.finditer(text):
            raw_url = match.group("url")
            # 去除末尾的标点符号
            cleaned = raw_url.rstrip('.,;:!?)')
            urls.append(cleaned)

        # 去重保持顺序
        seen = set()
        unique_urls = []
        for u in urls:
            if u not in seen:
                seen.add(u)
                unique_urls.append(u)

        return unique_urls

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        """
        从 URL 推断文件名

        1. 解析路径，取最后一段
        2. 如果没有扩展名，尝试根据 MIME 头或默认后缀
        3. 对 URL 编码进行解码
        """
        if not url:
            return ""

        parsed = urlparse(url)
        path = parsed.path
        if not path:
            return ""

        # 取最后一段
        filename = path.rstrip("/").split("/")[-1]
        # 解码 URL 编码
        filename = unquote(filename)

        # 如果没有扩展名，尝试添加 .html
        if not re.search(r"\.[a-zA-Z0-9]+$", filename):
            filename += ".html"

        return filename

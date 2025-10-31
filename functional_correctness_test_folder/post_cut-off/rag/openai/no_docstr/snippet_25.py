
from typing import List
import re
from urllib.parse import urlparse, unquote, parse_qs


class URLExtractor:
    '''URL提取器'''

    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        """
        将arXiv网页链接转换为PDF下载链接

        支持的输入形式:
            https://arxiv.org/abs/<id>
            https://arxiv.org/abs/<id>v<ver>
            https://arxiv.org/pdf/<id>.pdf
            https://arxiv.org/pdf/<id>v<ver>.pdf
        返回:
            https://arxiv.org/pdf/<id>.pdf
        """
        if not url:
            return url

        parsed = urlparse(url)
        if parsed.netloc != "arxiv.org":
            return url

        path = parsed.path
        # 处理 /abs/ 形式
        m_abs = re.match(r"^/abs/(?P<id>[^/]+)$", path)
        if m_abs:
            arxiv_id = m_abs.group("id")
            return f"https://arxiv.org/pdf/{arxiv_id}.pdf"

        # 处理 /pdf/ 形式，去掉可能的 .pdf 后缀
        m_pdf = re.match(r"^/pdf/(?P<id>[^/]+?)(\.pdf)?$", path)
        if m_pdf:
            arxiv_id = m_pdf.group("id")
            return f"https://arxiv.org/pdf/{arxiv_id}.pdf"

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

        # 简单的 URL 正则，兼容大多数情况
        url_pattern = re.compile(
            r"""
            (?P<url>
                (?:(?:https?|ftp|file)://)   # 协议
                [^\s<>"']+                   # 网址主体
            )
            """,
            re.VERBOSE | re.IGNORECASE,
        )
        return [m.group("url") for m in url_pattern.finditer(text)]

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        """
        从 URL 推断文件名

        1. 取路径最后一段
        2. 去除查询参数
        3. 如果没有文件名，返回 'download'
        """
        if not url:
            return "download"

        parsed = urlparse(url)
        path = parsed.path
        if not path or path.endswith("/"):
            # 末尾是目录，尝试从查询参数或默认名
            return "download"

        filename = path.rsplit("/", 1)[-1]
        # 去除可能的查询字符串
        filename = filename.split("?")[0]
        filename = filename.split("#")[0]
        # 对 URL 编码进行解码
        filename = unquote(filename)

        if not filename:
            return "download"
        return filename

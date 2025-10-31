
import re
from typing import List
from urllib.parse import urlparse, unquote
import os


class URLExtractor:
    '''URL提取器'''

    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        """
        将arXiv网页链接转换为PDF下载链接

        支持两种常见格式：
        - https://arxiv.org/abs/<id>
        - https://arxiv.org/pdf/<id>.pdf
        """
        if not url:
            return url

        parsed = urlparse(url)
        if parsed.netloc != "arxiv.org":
            return url

        # 处理 /abs/<id> 或 /pdf/<id>.pdf
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) >= 2:
            if path_parts[0] == "abs":
                arxiv_id = "/".join(path_parts[1:])
                return f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            if path_parts[0] == "pdf":
                # 可能已经是 pdf 链接
                if path_parts[1].endswith(".pdf"):
                    return url
                else:
                    arxiv_id = "/".join(path_parts[1:])
                    return f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        """
        从文本中提取 URL

        支持 http(s)://、ftp://、file:// 等协议
        """
        if not text:
            return []

        # 简单的 URL 正则，兼容常见情况
        url_pattern = re.compile(
            r"""
            (?P<url>
                (?:
                    https?://
                    | ftp://
                    | file://
                )
                [^\s<>"']+   # 直到空白或常见终止符
            )
            """,
            re.VERBOSE | re.IGNORECASE,
        )
        matches = url_pattern.finditer(text)
        urls = [m.group("url") for m in matches]
        return urls

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        """
        从 URL 推断文件名

        1. 取路径最后一段
        2. 去除查询字符串和片段
        3. 若为空，返回 'download'
        """
        if not url:
            return "download"

        parsed = urlparse(url)
        path = parsed.path
        # 去除末尾斜杠
        if path.endswith("/"):
            path = path[:-1]
        filename = os.path.basename(path)

        # 如果路径为空或仅为根目录
        if not filename:
            return "download"

        # 去除查询字符串和片段
        filename = unquote(filename.split("?")[0].split("#")[0])

        # 如果仍为空，使用默认名
        if not filename:
            return "download"

        return filename

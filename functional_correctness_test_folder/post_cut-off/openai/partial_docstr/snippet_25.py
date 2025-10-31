
import re
from typing import List
from urllib.parse import urlparse, unquote, urlunparse


class URLExtractor:
    '''URL提取器'''

    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        """
        将arXiv网页链接转换为PDF下载链接
        """
        if not url:
            return url

        parsed = urlparse(url)
        if 'arxiv.org' not in parsed.netloc:
            return url

        path = parsed.path
        # Handle /abs/xxxx.xxxx or /abs/xxxx.xxxxv1
        if path.startswith('/abs/'):
            # Replace /abs/ with /pdf/ and ensure .pdf suffix
            new_path = path.replace('/abs/', '/pdf/', 1)
            if not new_path.endswith('.pdf'):
                new_path += '.pdf'
            # Preserve query parameters if any
            new_parsed = parsed._replace(path=new_path)
            return urlunparse(new_parsed)

        # Handle /pdf/xxxx.xxxx or /pdf/xxxx.xxxx.pdf
        if path.startswith('/pdf/'):
            if not path.endswith('.pdf'):
                new_path = path + '.pdf'
                new_parsed = parsed._replace(path=new_path)
                return urlunparse(new_parsed)
            # Already a PDF link
            return url

        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        """
        从文本中提取所有 URL
        """
        if not text:
            return []

        # 简单的 URL 正则，排除常见的尾部标点
        url_pattern = re.compile(
            r'https?://[^\s\'"<>]+',
            re.IGNORECASE
        )
        raw_urls = url_pattern.findall(text)

        cleaned_urls = []
        for u in raw_urls:
            # 去除尾部常见标点
            u = u.rstrip('.,;!?)\'"')
            # 去除前导标点
            u = u.lstrip('(')
            cleaned_urls.append(u)

        return cleaned_urls

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        """
        从 URL 推断文件名
        """
        if not url:
            return ''

        parsed = urlparse(url)
        path = parsed.path
        if not path:
            return ''

        # 取路径最后一段
        filename = path.rsplit('/', 1)[-1]
        # 去掉可能的查询参数
        filename = filename.split('?', 1)[0]
        # 解码百分号编码
        filename = unquote(filename)

        # 如果文件名为空，尝试使用查询参数名
        if not filename:
            query = parsed.query
            if query:
                # 取第一个键
                key = query.split('=', 1)[0]
                filename = key

        # 如果仍为空，使用默认名
        if not filename:
            filename = 'downloaded_file'

        return filename

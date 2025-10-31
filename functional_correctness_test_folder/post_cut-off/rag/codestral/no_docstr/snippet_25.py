
import re
from typing import List
from urllib.parse import urlparse, parse_qs


class URLExtractor:
    '''URL提取器'''
    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        '''将arXiv网页链接转换为PDF下载链接'''
        parsed_url = urlparse(url)
        if 'arxiv.org' in parsed_url.netloc:
            path_parts = parsed_url.path.split('/')
            if len(path_parts) >= 3 and path_parts[1] == 'abs':
                paper_id = path_parts[2]
                return f"https://arxiv.org/pdf/{paper_id}.pdf"
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        '''从文本中提取URL'''
        url_pattern = re.compile(
            r'https?://'  # http:// or https://
            r'(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            r'(?:[/?#][^ \n]*)?'
        )
        urls = re.findall(url_pattern, text)
        return [cls.convert_arxiv_url(url) for url in urls]

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        '''从URL推断文件名'''
        parsed_url = urlparse(url)
        path = parsed_url.path
        if not path:
            return 'file'

        # 处理查询参数中的文件名
        query_params = parse_qs(parsed_url.query)
        if 'filename' in query_params:
            return query_params['filename'][0]

        # 从路径中提取文件名
        filename = path.split('/')[-1]
        if not filename:
            return 'file'

        # 处理URL编码
        filename = re.sub(r'%20', ' ', filename)

        # 移除查询参数
        filename = filename.split('?')[0]

        return filename if filename else 'file'

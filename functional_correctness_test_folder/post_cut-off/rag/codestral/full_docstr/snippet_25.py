
import re
from typing import List
from urllib.parse import urlparse, parse_qs


class URLExtractor:
    '''URL提取器'''
    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        '''将arXiv网页链接转换为PDF下载链接'''
        if 'arxiv.org' not in url:
            return url

        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split('/')

        if len(path_parts) >= 3 and path_parts[1] == 'abs':
            paper_id = path_parts[2]
            return f'https://arxiv.org/pdf/{paper_id}.pdf'

        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        '''从文本中提取URL'''
        url_pattern = re.compile(
            r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
            r'(?:/[-\w./?%&=#]*)?'
            r'(?:\.[a-zA-Z]{2,4}\b(?:/[-\w./?%&=#]*)?)'
        )
        urls = url_pattern.findall(text)
        return [cls.convert_arxiv_url(url) for url in urls]

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        '''从URL推断文件名'''
        parsed_url = urlparse(url)
        path = parsed_url.path
        filename = path.split('/')[-1]

        if not filename or '.' not in filename:
            if 'arxiv.org' in url and '/pdf/' in path:
                paper_id = path.split('/')[-1].split('.')[0]
                filename = f'{paper_id}.pdf'
            else:
                filename = 'downloaded_file'

        return filename

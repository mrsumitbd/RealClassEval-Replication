
import re
from typing import List


class URLExtractor:
    '''URL提取器'''

    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        '''将arXiv网页链接转换为PDF下载链接'''
        # Match arXiv URLs of the form https://arxiv.org/abs/<id> or https://arxiv.org/pdf/<id>.pdf
        pattern = r'https?://arxiv\.org/(abs|pdf)/(?P<id>[^/]+)(?:\.pdf)?'
        match = re.match(pattern, url)
        if match:
            arxiv_id = match.group('id')
            return f'https://arxiv.org/pdf/{arxiv_id}.pdf'
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        '''从文本中提取URL'''
        # Simple regex to capture http/https URLs
        url_pattern = r'https?://[^\s\'"<>]+'
        return re.findall(url_pattern, text)

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        '''从URL推断文件名'''
        # Strip query parameters and fragments
        path = url.split('?', 1)[0].split('#', 1)[0]
        # Get the last component after '/'
        filename = path.rstrip('/').split('/')[-1]
        if not filename:
            return 'download'
        return filename

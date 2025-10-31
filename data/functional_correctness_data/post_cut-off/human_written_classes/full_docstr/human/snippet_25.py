from typing import List, Dict, Optional, Any
import re
from datetime import datetime
import os
from urllib.parse import urlparse, unquote

class URLExtractor:
    """URL提取器"""
    URL_PATTERNS = ["https?://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+(?:/(?:[-\\w._~!$&\\'()*+,;=:@]|%[\\da-fA-F]{2})*)*(?:\\?(?:[-\\w._~!$&\\'()*+,;=:@/?]|%[\\da-fA-F]{2})*)?(?:#(?:[-\\w._~!$&\\'()*+,;=:@/?]|%[\\da-fA-F]{2})*)?", "ftp://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+(?:/(?:[-\\w._~!$&\\'()*+,;=:@]|%[\\da-fA-F]{2})*)*", "(?<!\\S)(?:www\\.)?[-\\w]+(?:\\.[-\\w]+)+/(?:[-\\w._~!$&\\'()*+,;=:@/]|%[\\da-fA-F]{2})+"]

    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        """将arXiv网页链接转换为PDF下载链接"""
        arxiv_pattern = 'arxiv\\.org/abs/(\\d+\\.\\d+)(?:v\\d+)?'
        match = re.search(arxiv_pattern, url, re.IGNORECASE)
        if match:
            paper_id = match.group(1)
            return f'https://arxiv.org/pdf/{paper_id}.pdf'
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        """从文本中提取URL"""
        urls = []
        at_url_pattern = '@(https?://[^\\s]+)'
        at_matches = re.findall(at_url_pattern, text, re.IGNORECASE)
        for match in at_matches:
            url = cls.convert_arxiv_url(match.rstrip('/'))
            urls.append(url)
        for pattern in cls.URL_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if not match.startswith(('http://', 'https://', 'ftp://')):
                    if match.startswith('www.'):
                        match = 'https://' + match
                    else:
                        match = 'https://' + match
                url = cls.convert_arxiv_url(match.rstrip('/'))
                urls.append(url)
        seen = set()
        unique_urls = []
        for url in urls:
            if url not in seen:
                seen.add(url)
                unique_urls.append(url)
        return unique_urls

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        """从URL推断文件名"""
        parsed = urlparse(url)
        path = unquote(parsed.path)
        filename = os.path.basename(path)
        if 'arxiv.org' in parsed.netloc and '/pdf/' in path:
            if filename:
                if not filename.lower().endswith(('.pdf', '.doc', '.docx', '.txt')):
                    filename = f'{filename}.pdf'
            else:
                path_parts = [p for p in path.split('/') if p]
                if path_parts and path_parts[-1]:
                    filename = f'{path_parts[-1]}.pdf'
                else:
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f'arxiv_paper_{timestamp}.pdf'
        elif not filename or '.' not in filename:
            domain = parsed.netloc.replace('www.', '').replace('.', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            if not path or path == '/':
                filename = f'{domain}_{timestamp}.html'
            else:
                path_parts = [p for p in path.split('/') if p]
                if path_parts:
                    filename = f'{path_parts[-1]}_{timestamp}'
                else:
                    filename = f'{domain}_{timestamp}'
                if '.' not in filename:
                    if '/pdf/' in path.lower() or path.lower().endswith('pdf'):
                        filename += '.pdf'
                    elif any((ext in path.lower() for ext in ['/doc/', '/word/', '.docx'])):
                        filename += '.docx'
                    elif any((ext in path.lower() for ext in ['/ppt/', '/powerpoint/', '.pptx'])):
                        filename += '.pptx'
                    elif any((ext in path.lower() for ext in ['/csv/', '.csv'])):
                        filename += '.csv'
                    elif any((ext in path.lower() for ext in ['/zip/', '.zip'])):
                        filename += '.zip'
                    else:
                        filename += '.html'
        return filename
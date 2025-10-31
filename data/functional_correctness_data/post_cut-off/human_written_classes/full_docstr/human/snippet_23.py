from typing import Dict, List, Optional
import re

class GitHubURLExtractor:
    """提取GitHub URL的工具类"""

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        """从文本中提取GitHub URLs"""
        patterns = ['https?://github\\.com/[\\w\\-\\.]+/[\\w\\-\\.]+(?:\\.git)?', 'git@github\\.com:[\\w\\-\\.]+/[\\w\\-\\.]+(?:\\.git)?', '(?<!\\S)(?<!/)(?<!\\.)([\\w\\-\\.]+/[\\w\\-\\.]+)(?!/)(?!\\S)']
        urls = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                if match.startswith('git@'):
                    url = match.replace('git@github.com:', 'https://github.com/')
                elif match.startswith('http'):
                    url = match
                elif '/' in match and (not any((x in match for x in ['./', '../', 'deepcode_lab', 'tools']))):
                    parts = match.split('/')
                    if len(parts) == 2 and all((part.replace('-', '').replace('_', '').isalnum() for part in parts)) and (not any((part.startswith('.') for part in parts))):
                        url = f'https://github.com/{match}'
                    else:
                        continue
                else:
                    continue
                url = url.rstrip('.git')
                url = url.rstrip('/')
                if 'github.com/github.com/' in url:
                    url = url.replace('github.com/github.com/', 'github.com/')
                urls.append(url)
        return list(set(urls))

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        """从文本中提取目标路径"""
        patterns = ['(?:to|into|in|at)\\s+(?:folder|directory|path)?\\s*["\\\']?([^\\s"\\\']+)["\\\']?', '(?:save|download|clone)\\s+(?:to|into|at)\\s+["\\\']?([^\\s"\\\']+)["\\\']?', '(?:到|在|保存到|下载到|克隆到)\\s*["\\\']?([^\\s"\\\']+)["\\\']?']
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                path = match.group(1).strip('。，,.')
                if path and path.lower() not in ['here', 'there', 'current', 'local', '这里', '当前', '本地']:
                    return path
        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        """从URL推断仓库名称"""
        url = url.rstrip('.git')
        if 'github.com' in url:
            parts = url.split('/')
            if len(parts) >= 2:
                return parts[-1]
        return 'repository'

import re
from typing import List


class LocalPathExtractor:

    @staticmethod
    def is_local_path(path: str) -> bool:
        pattern = r'^[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*$'
        return bool(re.match(pattern, path))

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        pattern = r'[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*'
        return re.findall(pattern, text)


import re
from typing import List


class LocalPathExtractor:

    @staticmethod
    def is_local_path(path: str) -> bool:
        # Simple regex to check for local file paths
        return re.match(r'^[a-zA-Z]:\\|/', path) is not None

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        # Regex to find potential local file paths in the text
        local_path_pattern = r'[a-zA-Z]:\\[^\s"]+|\/[^\s"]+'
        return re.findall(local_path_pattern, text)

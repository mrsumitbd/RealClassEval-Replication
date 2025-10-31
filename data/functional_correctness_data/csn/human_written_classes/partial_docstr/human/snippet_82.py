from pathlib import Path
from typing import Any, Dict, Optional, Tuple

class Trie:
    """
    A prefix tree to store the paths of all config files and to search the nearest config
    associated with each file
    """

    def __init__(self, config_file: str='', config_data: Optional[Dict[str, Any]]=None) -> None:
        self.root: TrieNode = TrieNode(config_file, config_data)

    def insert(self, config_file: str, config_data: Dict[str, Any]) -> None:
        resolved_config_path_as_tuple = Path(config_file).parent.resolve().parts
        temp = self.root
        for path in resolved_config_path_as_tuple:
            if path not in temp.nodes:
                temp.nodes[path] = TrieNode()
            temp = temp.nodes[path]
        temp.config_info = (config_file, config_data)

    def search(self, filename: str) -> Tuple[str, Dict[str, Any]]:
        """
        Returns the closest config relative to filename by doing a depth
        first search on the prefix tree.
        """
        resolved_file_path_as_tuple = Path(filename).resolve().parts
        temp = self.root
        last_stored_config: Tuple[str, Dict[str, Any]] = ('', {})
        for path in resolved_file_path_as_tuple:
            if temp.config_info[0]:
                last_stored_config = temp.config_info
            if path not in temp.nodes:
                break
            temp = temp.nodes[path]
        return last_stored_config
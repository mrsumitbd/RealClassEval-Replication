from typing import Any, Dict, List
import json

class WordObj:

    def __init__(self) -> None:
        self.text: str = None
        self.begin_time: int = None
        self.end_time: int = None
        self.fixed: bool = False
        self._raw_data = None

    @staticmethod
    def from_json(json_data: Dict[str, Any]):
        """Create a Word object from a JSON dictionary.
        """
        word = WordObj()
        word.text = json_data['text']
        word.begin_time = json_data['begin_time']
        word.end_time = json_data['end_time']
        word.fixed = json_data['fixed']
        word._raw_data = json_data
        return word

    def __str__(self) -> str:
        return 'Word: ' + json.dumps(self._raw_data, ensure_ascii=False)

    def __repr__(self):
        return self.__str__()
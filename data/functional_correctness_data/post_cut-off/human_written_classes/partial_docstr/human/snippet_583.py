from typing import Any, Dict, List
import json

class SentenceBaseObj:

    def __init__(self) -> None:
        self.sentence_id: int = -1
        self.text: str = None
        self.begin_time: int = None
        self.end_time: int = None
        self.words: List[WordObj] = []
        self._raw_data = None

    @staticmethod
    def from_json(json_data: Dict[str, Any]):
        """Create a SentenceBase object from a JSON dictionary.
        """
        sentence = SentenceBaseObj()
        sentence.sentence_id = json_data['sentence_id']
        sentence.text = json_data['text']
        sentence.begin_time = json_data['begin_time']
        if json_data.get('end_time') is not None:
            sentence.end_time = json_data['end_time']
        else:
            sentence.end_time = json_data['current_time']
        sentence.words = [WordObj.from_json(word) for word in json_data['words']]
        sentence._raw_data = json_data
        return sentence

    def __str__(self) -> str:
        return json.dumps(self._raw_data, ensure_ascii=False)

    def __repr__(self):
        return self.__str__()
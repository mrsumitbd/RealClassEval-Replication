from typing import Dict, Any, List, Optional

class DailyTimeline:

    def __init__(self, id: int, dateTime: str, content: str, noteIds: List[int]):
        self.id = id
        self.date_time = dateTime
        self.content = content.strip()
        self.note_ids = noteIds

    def _desc_(self) -> str:
        """Returns a string representation of the daily timeline.

        Returns:
            str: Formatted string representation.
        """
        return f'- [{self.date_time}] {self.content}'.strip()

    def to_dict(self) -> Dict[str, Any]:
        """Converts the DailyTimeline object to a dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of the DailyTimeline.
        """
        return {'id': self.id, 'dateTime': self.date_time, 'content': self.content, 'noteIds': self.note_ids}
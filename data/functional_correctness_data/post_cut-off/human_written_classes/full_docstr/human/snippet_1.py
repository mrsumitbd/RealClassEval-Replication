from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class GlobalBioDTO:
    """Global biography data transfer object"""
    content: str
    content_third_view: str
    summary: str
    summary_third_view: str
    create_time: datetime
    shades: List[Dict] = None

    @classmethod
    def from_model(cls, model: 'L1Bio') -> 'GlobalBioDTO':
        """
        Create DTO from database model

        Args:
            model (L1Bio): database model object

        Returns:
            GlobalBioDTO: data transfer object
        """
        return cls(content=model.content, content_third_view=model.content_third_view, summary=model.summary, summary_third_view=model.summary_third_view, create_time=model.create_time, shades=[])

    def to_dict(self) -> dict:
        """
        Convert to dictionary format

        Returns:
            dict: dictionary format data
        """
        return {'content': self.content, 'content_third_view': self.content_third_view, 'summary': self.summary, 'summary_third_view': self.summary_third_view, 'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'), 'shades': self.shades or []}
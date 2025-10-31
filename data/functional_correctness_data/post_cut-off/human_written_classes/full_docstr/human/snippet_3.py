from dataclasses import dataclass
from datetime import datetime

@dataclass
class StatusBioDTO:
    """Status biography data transfer object"""
    content: str
    content_third_view: str
    summary: str
    summary_third_view: str
    create_time: datetime
    update_time: datetime

    @classmethod
    def from_model(cls, model: 'StatusBiography') -> 'StatusBioDTO':
        """Create DTO from database model

        Args:
            model (StatusBiography): database model object

        Returns:
            StatusBioDTO: data transfer object
        """
        return cls(content=model.content, content_third_view=model.content_third_view, summary=model.summary, summary_third_view=model.summary_third_view, create_time=model.create_time, update_time=model.update_time)

    def to_dict(self) -> dict:
        """Convert to dictionary format

        Returns:
            dict: dictionary format data
        """
        return {'content': self.content, 'content_third_view': self.content_third_view, 'summary': self.summary, 'summary_third_view': self.summary_third_view, 'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'), 'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')}
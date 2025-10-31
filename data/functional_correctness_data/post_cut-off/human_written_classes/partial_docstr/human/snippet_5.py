from datetime import datetime
from typing import Dict, Any, List, Optional

class MonthlyTimeline:

    def __init__(self, id: int, monthDate: str, title: str, dailyTimelines: List[Dict[str, Any]]):
        self.id = id
        self.month_date = monthDate
        self.title = title
        daily_timelines = [DailyTimeline(**daily_timeline) for daily_timeline in dailyTimelines]
        self.daily_timelines = sorted(daily_timelines, key=lambda x: datetime.strptime(x.date_time, DATE_TIME_FORMAT))

    def _desc_(self) -> str:
        """Returns a string representation of the monthly timeline.

        Returns:
            str: Formatted string representation.
        """
        return f'** {self.month_date} **\n' + '\n'.join([daily_timeline._desc_() for daily_timeline in self.daily_timelines])

    def _preview_(self, preview_num: int=0) -> str:
        """Generates a preview of the monthly timeline.

        Args:
            preview_num: Number of daily timelines to include in the preview.

        Returns:
            str: Preview string of the monthly timeline.
        """
        preview_statement = f'[{self.month_date}] {self.title}\n'
        for daily_timeline in self.daily_timelines[:preview_num]:
            preview_statement += daily_timeline._desc_() + '\n'
        return preview_statement

    def to_dict(self) -> Dict[str, Any]:
        """Converts the MonthlyTimeline object to a dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of the MonthlyTimeline.
        """
        return {'id': self.id, 'monthDate': self.month_date, 'title': self.title, 'dailyTimelines': [daily_timeline.to_dict() for daily_timeline in self.daily_timelines]}
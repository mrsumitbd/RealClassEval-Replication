from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass
class BaseAnalysis:
    """Description of base analysis module of report.
    Overall info about report.

    Attributes
        title (str): Title of report.
        date_start (Union[datetime, List[datetime]]): Start of generating description.
        date_end (Union[datetime, List[datetime]]): End of generating description.
    """
    title: str
    date_start: Union[datetime, List[datetime]]
    date_end: Union[datetime, List[datetime]]

    def __init__(self, title: str, date_start: datetime, date_end: datetime) -> None:
        self.title = title
        self.date_start = date_start
        self.date_end = date_end

    @property
    def duration(self) -> Union[timedelta, List[timedelta]]:
        if isinstance(self.date_start, datetime) and isinstance(self.date_end, datetime):
            return self.date_end - self.date_start
        if isinstance(self.date_start, list) and isinstance(self.date_end, list):
            return [self.date_end[i] - self.date_start[i] for i in range(len(self.date_start))]
        else:
            raise TypeError()
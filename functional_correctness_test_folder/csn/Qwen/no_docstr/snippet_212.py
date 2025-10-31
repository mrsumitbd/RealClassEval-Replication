
from datetime import date, timedelta
from typing import Dict, Union
from chinese_calendar import is_holiday, is_workday, LunarDate


class ThreeNineUtils:

    @staticmethod
    def get_39days(year: int) -> Dict[str, date]:
        start_date = date(year, 3, 1)
        days = {}
        for i in range(39):
            current_date = start_date + timedelta(days=i)
            days[f"Day_{i+1}"] = current_date
        return days

    @staticmethod
    def get_39label(date_obj: Union[date, LunarDate]) -> str:
        if isinstance(date_obj, LunarDate):
            date_obj = date_obj.toSolarDate()
        if is_holiday(date_obj):
            return "Holiday"
        elif is_workday(date_obj):
            return "Workday"
        else:
            return "Unknown"

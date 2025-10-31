
from datetime import date, timedelta
from typing import Dict, Union
from lunarcalendar import LunarDate


class ThreeNineUtils:

    @staticmethod
    def get_39days(year: int) -> Dict[str, date]:
        result = {}
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)

        current_date = start_date
        while current_date <= end_date:
            if current_date.month in [3, 9]:
                result[current_date.strftime("%Y-%m-%d")] = current_date
            current_date += timedelta(days=1)

        return result

    @staticmethod
    def get_39label(date_obj: Union[date, LunarDate]) -> str:
        if isinstance(date_obj, LunarDate):
            date_obj = date_obj.toSolarDate()

        if date_obj.month in [3, 9]:
            return "39"
        else:
            return ""

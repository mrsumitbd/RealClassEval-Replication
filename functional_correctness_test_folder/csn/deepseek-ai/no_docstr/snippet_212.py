
from datetime import date
from typing import Dict, Union
from lunarcalendar import LunarDate


class ThreeNineUtils:

    @staticmethod
    def get_39days(year: int) -> Dict[str, date]:
        # Approximate, may need adjustment
        winter_solstice = date(year, 12, 22)
        # Calculate the 3rd and 9th periods (each 9 days)
        third_day = winter_solstice.replace(day=winter_solstice.day + 18)
        ninth_day = winter_solstice.replace(day=winter_solstice.day + 81)
        return {
            "3rd_day_start": winter_solstice.replace(day=winter_solstice.day + 18),
            "3rd_day_end": winter_solstice.replace(day=winter_solstice.day + 26),
            "9th_day_start": winter_solstice.replace(day=winter_solstice.day + 81),
            "9th_day_end": winter_solstice.replace(day=winter_solstice.day + 89),
        }

    @staticmethod
    def get_39label(date_obj: Union[date, LunarDate]) -> str:
        if isinstance(date_obj, LunarDate):
            date_obj = date_obj.to_date()

        year = date_obj.year
        periods = ThreeNineUtils.get_39days(year)

        if periods["3rd_day_start"] <= date_obj <= periods["3rd_day_end"]:
            return "3rd_day"
        elif periods["9th_day_start"] <= date_obj <= periods["9th_day_end"]:
            return "9th_day"
        else:
            return "not_39day"

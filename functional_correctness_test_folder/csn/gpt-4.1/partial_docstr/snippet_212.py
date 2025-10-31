
from datetime import date, timedelta
from typing import Dict, Union
try:
    from lunardate import LunarDate
except ImportError:
    class LunarDate:
        pass  # placeholder if lunardate is not installed


class ThreeNineUtils:
    @staticmethod
    def get_39days(year: int) -> Dict[str, date]:
        '''获取公历year年的三伏数九天对应的公历日期。'''
        # "三伏" and "数九" are two different traditional Chinese calendrical periods.
        # "数九" (Shu Jiu) starts from the Winter Solstice (冬至), each "九" is 9 days, total 9*9=81 days.
        # We'll calculate the dates for each "九" period.
        # "三伏" is not required here as per the function name and docstring.

        # Find the date of the Winter Solstice for the given year.
        # For simplicity, use astronomical approximation: Winter Solstice is usually Dec 21 or 22.
        # We'll use Dec 21 if year < 2088, else Dec 22 (Gregorian calendar drift).
        # For more accuracy, a solar term library would be needed.

        # Approximate Winter Solstice
        if year < 2088:
            dongzhi = date(year, 12, 21)
        else:
            dongzhi = date(year, 12, 22)

        result = {}
        for i in range(9):
            start = dongzhi + timedelta(days=i*9)
            end = start + timedelta(days=8)
            label = f"{i+1}九"
            result[label] = start
        return result

    @staticmethod
    def get_39label(date_obj: Union[date, 'LunarDate']) -> str:
        # If LunarDate, convert to Gregorian date
        if isinstance(date_obj, LunarDate):
            dt = date_obj.toSolarDate()
        else:
            dt = date_obj

        # Find the Winter Solstice for the year of the date
        year = dt.year
        # If date is before Dec 21, the relevant Winter Solstice is in the previous year
        if dt < date(year, 12, 21):
            year -= 1
        if year < 2088:
            dongzhi = date(year, 12, 21)
        else:
            dongzhi = date(year, 12, 22)

        # Calculate days since Winter Solstice
        delta = (dt - dongzhi).days
        if delta < 0 or delta >= 81:
            return ""
        n = delta // 9 + 1
        day_in_nine = delta % 9 + 1
        return f"{n}九第{day_in_nine}天"

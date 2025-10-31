from datetime import date, timedelta
from typing import Dict, Union

try:
    from lunardate import LunarDate  # type: ignore
except Exception:  # pragma: no cover
    LunarDate = None  # type: ignore


class ThreeNineUtils:
    _CN_NUMS = ("一", "二", "三", "四", "五", "六", "七", "八", "九")

    @staticmethod
    def _dongzhi_start(year: int) -> date:
        # Approximate start of ShuJiu at winter solstice (Dongzhi).
        # Use Dec 21 as a simple, consistent approximation.
        return date(year, 12, 21)

    @staticmethod
    def _label_for_index(idx: int) -> str:
        nine = idx // 9 + 1  # 1..9
        day_in_nine = idx % 9 + 1  # 1..9
        return f"{ThreeNineUtils._CN_NUMS[nine - 1]}九第{day_in_nine}天"

    @staticmethod
    def get_39days(year: int) -> Dict[str, date]:
        start = ThreeNineUtils._dongzhi_start(year)
        days: Dict[str, date] = {}
        for i in range(81):
            label = ThreeNineUtils._label_for_index(i)
            days[label] = start + timedelta(days=i)
        return days

    @staticmethod
    def get_39label(date_obj: Union[date, "LunarDate"]) -> str:
        if LunarDate is not None and isinstance(date_obj, LunarDate):
            d = date_obj.toSolarDate()
        elif isinstance(date_obj, date):
            d = date_obj
        else:
            raise TypeError("date_obj must be datetime.date or LunarDate")

        start_this_year = ThreeNineUtils._dongzhi_start(d.year)
        if d >= start_this_year:
            start = start_this_year
        else:
            start = ThreeNineUtils._dongzhi_start(d.year - 1)

        delta = (d - start).days
        if 0 <= delta < 81:
            return ThreeNineUtils._label_for_index(delta)
        return ""

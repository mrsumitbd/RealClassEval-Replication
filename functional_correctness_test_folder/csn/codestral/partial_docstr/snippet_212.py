
from typing import Dict, Union
from datetime import date
from lunarcalendar import LunarDate


class ThreeNineUtils:

    @staticmethod
    def get_39days(year: int) -> Dict[str, date]:
        # 计算公历year年的三伏数九天对应的公历日期
        # 这里使用了一个简化的算法，实际应用中可能需要更精确的计算方法
        # 例如，可以参考《中国气象》中的计算方法
        # 以下是一个示例实现，可能不完全准确
        start_date = date(year, 7, 1)
        end_date = date(year, 8, 31)
        delta = end_date - start_date
        days = [start_date + timedelta(days=i) for i in range(delta.days + 1)]
        # 选择三伏数九天，这里简单地选择每月的第15天
        three_nine_days = [day for day in days if day.day == 15]
        return {f"三伏数九天{i+1}": day for i, day in enumerate(three_nine_days)}

    @staticmethod
    def get_39label(date_obj: Union[date, LunarDate]) -> str:
        # 判断date_obj是否为三伏数九天
        # 这里同样使用了一个简化的算法
        if isinstance(date_obj, LunarDate):
            date_obj = date_obj.toSolarDate()
        year = date_obj.year
        three_nine_days = ThreeNineUtils.get_39days(year)
        if date_obj in three_nine_days.values():
            return "三伏数九天"
        else:
            return "非三伏数九天"

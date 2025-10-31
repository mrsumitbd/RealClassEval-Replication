
from typing import Dict, Union
from datetime import date
from lunarcalendar import LunarDate


class ThreeNineUtils:
    '''三伏数九天工具函数
    '''
    @staticmethod
    def get_39days(year: int) -> Dict[str, date]:
        '''获取公历year年的三伏数九天对应的公历日期。
        '''
        # 计算三伏数九天的公历日期
        # 这里使用了一个简化的算法，实际应用中可能需要更精确的计算
        # 例如，可以使用天文算法或历法库来获取更准确的日期
        # 这里仅作为示例
        first_day = date(year, 7, 1)
        second_day = date(year, 7, 2)
        third_day = date(year, 7, 3)
        fourth_day = date(year, 7, 4)
        fifth_day = date(year, 7, 5)
        sixth_day = date(year, 7, 6)
        seventh_day = date(year, 7, 7)
        eighth_day = date(year, 7, 8)
        ninth_day = date(year, 7, 9)

        return {
            '初伏第一天': first_day,
            '初伏第二天': second_day,
            '初伏第三天': third_day,
            '中伏第一天': fourth_day,
            '中伏第二天': fifth_day,
            '中伏第三天': sixth_day,
            '末伏第一天': seventh_day,
            '末伏第二天': eighth_day,
            '末伏第三天': ninth_day
        }

    @staticmethod
    def get_39label(date_obj: Union[date, LunarDate]) -> str:
        '''返回三伏数九天对应的标签，如果不是，返回空字符串。
        '''
        if isinstance(date_obj, LunarDate):
            date_obj = date_obj.toSolarDate()

        year = date_obj.year
        three_nine_days = ThreeNineUtils.get_39days(year)

        for label, day in three_nine_days.items():
            if date_obj == day:
                return label

        return ''

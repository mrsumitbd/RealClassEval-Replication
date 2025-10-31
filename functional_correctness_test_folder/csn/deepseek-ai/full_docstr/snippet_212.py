
from typing import Dict, Union
from datetime import date, timedelta
from lunarcalendar import LunarDate


class ThreeNineUtils:
    '''三伏数九天工具函数
    '''
    @staticmethod
    def get_39days(year: int) -> Dict[str, date]:
        '''获取公历year年的三伏数九天对应的公历日期。
        '''
        def get_solar_term_date(y, term_index):
            # Simplified placeholder for solar term calculation
            # In practice, this should use accurate astronomical calculations
            base_date = date(y, 1, 1)
            return base_date + timedelta(days=term_index * 15)

        # Calculate 初伏 (first fu), 中伏 (middle fu), 末伏 (last fu)
        # 初伏 is the first 庚日 after 夏至 (summer solstice, ~June 21)
        summer_solstice = date(year, 6, 21)
        first_fu = summer_solstice + \
            timedelta(days=(7 - (summer_solstice.weekday() + 1) % 10) % 10)

        # 中伏 is 10 or 20 days after 初伏 (depending on the year)
        middle_fu = first_fu + timedelta(days=10)

        # 末伏 is the first 庚日 after 立秋 (autumn start, ~Aug 7)
        autumn_start = date(year, 8, 7)
        last_fu = autumn_start + \
            timedelta(days=(7 - (autumn_start.weekday() + 1) % 10) % 10)

        # Calculate 数九 days (winter 9-day periods)
        winter_solstice = date(year, 12, 21)
        first_nine = winter_solstice
        second_nine = first_nine + timedelta(days=9)
        third_nine = second_nine + timedelta(days=9)
        fourth_nine = third_nine + timedelta(days=9)

        return {
            '初伏': first_fu,
            '中伏': middle_fu,
            '末伏': last_fu,
            '一九': first_nine,
            '二九': second_nine,
            '三九': third_nine,
            '四九': fourth_nine,
        }

    @staticmethod
    def get_39label(date_obj: Union[date, LunarDate]) -> str:
        '''返回三伏数九天对应的标签，如果不是，返回空字符串。
        '''
        if isinstance(date_obj, LunarDate):
            date_obj = date_obj.to_date()

        year = date_obj.year
        days = ThreeNineUtils.get_39days(year)

        for label, day in days.items():
            if date_obj == day:
                return label

        # Check for ranges in 数九 days
        winter_solstice = date(year, 12, 21)
        if date_obj >= winter_solstice:
            delta = (date_obj - winter_solstice).days
            if delta < 9:
                return '一九'
            elif delta < 18:
                return '二九'
            elif delta < 27:
                return '三九'
            elif delta < 36:
                return '四九'

        return ''

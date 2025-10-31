
from datetime import date
from typing import Dict, Union
from chinese_calendar import is_holiday, get_holiday_detail, Lunar


class ThreeNineUtils:
    '''三伏数九天工具函数
    '''
    @staticmethod
    def get_39days(year: int) -> Dict[str, date]:
        '''获取公历year年的三伏数九天对应的公历日期。
        '''
        def find_nth_day_of_lunar_month(year, month, nth_day):
            day = 1
            while nth_day > 0:
                lunar_date = Lunar(year, month, day)
                if lunar_date.is_leap_month:
                    day += 1
                    continue
                if lunar_date.month == month:
                    nth_day -= 1
                if nth_day == 0:
                    return lunar_date.toSolarDate()
                day += 1

        start_of_summer = find_nth_day_of_lunar_month(year, 6, 1)
        start_of_summer_lunar = Lunar.fromSolarDate(
            start_of_summer.year, start_of_summer.month, start_of_summer.day)
        baihuo_day = start_of_summer_lunar.day + 10
        baihuo_date = start_of_summer_lunar.toSolarDate()

        first_fu_start = baihuo_date
        first_fu_end = find_nth_day_of_lunar_month(year, 6, baihuo_day + 9)
        second_fu_start = find_nth_day_of_lunar_month(year, 6, baihuo_day + 10)
        second_fu_end = find_nth_day_of_lunar_month(year, 6, baihuo_day + 19)
        third_fu_start = find_nth_day_of_lunar_month(year, 6, baihuo_day + 20)
        third_fu_end = find_nth_day_of_lunar_month(year, 6, baihuo_day + 29)

        start_of_winter = find_nth_day_of_lunar_month(year + 1, 11, 1)
        start_of_winter_lunar = Lunar.fromSolarDate(
            start_of_winter.year, start_of_winter.month, start_of_winter.day)
        jiuhuo_day = start_of_winter_lunar.day + 9
        jiuhuo_date = start_of_winter_lunar.toSolarDate()

        first_jiu_start = jiuhuo_date
        first_jiu_end = find_nth_day_of_lunar_month(
            year + 1, 11, jiuhuo_day + 8)
        second_jiu_start = find_nth_day_of_lunar_month(
            year + 1, 11, jiuhuo_day + 9)
        second_jiu_end = find_nth_day_of_lunar_month(
            year + 1, 11, jiuhuo_day + 17)
        third_jiu_start = find_nth_day_of_lunar_month(
            year + 1, 11, jiuhuo_day + 18)
        third_jiu_end = find_nth_day_of_lunar_month(
            year + 1, 11, jiuhuo_day + 26)
        fourth_jiu_start = find_nth_day_of_lunar_month(
            year + 1, 11, jiuhuo_day + 27)
        fourth_jiu_end = find_nth_day_of_lunar_month(
            year + 1, 11, jiuhuo_day + 35)

        return {
            'first_fu_start': first_fu_start,
            'first_fu_end': first_fu_end,
            'second_fu_start': second_fu_start,
            'second_fu_end': second_fu_end,
            'third_fu_start': third_fu_start,
            'third_fu_end': third_fu_end,
            'first_jiu_start': first_jiu_start,
            'first_jiu_end': first_jiu_end,
            'second_jiu_start': second_jiu_start,
            'second_jiu_end': second_jiu_end,
            'third_jiu_start': third_jiu_start,
            'third_jiu_end': third_jiu_end,
            'fourth_jiu_start': fourth_jiu_start,
            'fourth_jiu_end': fourth_jiu_end,
        }

    @staticmethod
    def get_39label(date_obj: Union[date, Lunar]) -> str:
        '''返回三伏数九天对应的标签，如果不是，返回空字符串。
        '''
        if isinstance(date_obj, Lunar):
            date_obj = date_obj.toSolarDate()

        year = date_obj.year
        days = ThreeNineUtils.get_39days(year)

        for key, value in days.items():
            if isinstance(value, tuple):
                start, end = value
                if start <= date_obj <= end:
                    return key
            else:
                if date_obj == value:
                    return key

        return ''

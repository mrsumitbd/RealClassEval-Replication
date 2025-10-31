
from datetime import date, timedelta
from typing import Dict, Union
from chinese_calendar import is_holiday, get_holiday_detail, Lunar


class ThreeNineUtils:

    @staticmethod
    def get_39days(year: int) -> Dict[str, date]:
        '''获取公历year年的三伏数九天对应的公历日期。
        '''
        def find_nth_day_of_month(year, month, nth, weekday):
            day = 1
            count = 0
            while count < nth:
                if date(year, month, day).weekday() == weekday:
                    count += 1
                if count == nth:
                    return date(year, month, day)
                day += 1

        start_of_summer = find_nth_day_of_month(year, 6, 3, 0)  # 第三个周一
        start_of_first_frost = find_nth_day_of_month(year, 11, 3, 0)  # 第三个周一

        first_frost_lunar = Lunar.fromSolarDate(
            start_of_first_frost.year, start_of_first_frost.month, start_of_first_frost.day)
        first_nine_day = first_frost_lunar.toSolarDate().to_date() - timedelta(days=9)

        three_nine_days = {
            'first_nine_day': first_nine_day,
            'start_of_summer': start_of_summer,
            'start_of_first_frost': start_of_first_frost
        }

        return three_nine_days

    @staticmethod
    def get_39label(date_obj: Union[date, Lunar]) -> str:
        if isinstance(date_obj, Lunar):
            date_obj = date_obj.toSolarDate().to_date()

        year = date_obj.year
        three_nine_days = ThreeNineUtils.get_39days(year)
        first_nine_day = three_nine_days['first_nine_day']
        start_of_summer = three_nine_days['start_of_summer']
        start_of_first_frost = three_nine_days['start_of_first_frost']

        if first_nine_day <= date_obj <= first_nine_day + timedelta(days=89):
            nine_day_index = (date_obj - first_nine_day).days // 9 + 1
            return f"数九第{nine_day_index}九"
        elif start_of_summer <= date_obj <= start_of_first_frost:
            return "三伏天"
        else:
            return "非三伏数九天"

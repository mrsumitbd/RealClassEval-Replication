
from typing import Dict, Union
from datetime import date
from lunardate import LunarDate


class ThreeNineUtils:

    @staticmethod
    def get_39days(year: int) -> Dict[str, date]:
        '''获取公历year年的三伏数九天对应的公历日期。
        '''
        from lunardate import SolarTerm
        start_date = date(year, 7, 1)
        end_date = date(year + 1, 2, 15)
        curr_date = start_date
        three_nine_days = {}
        is_fu = False
        fu_count = 0
        is_jiu = False
        jiu_count = 0
        while curr_date <= end_date:
            lunar_date = LunarDate.from_date(curr_date)
            if SolarTerm.from_lunar_date(lunar_date).name == '夏至':
                xia_zhi = lunar_date
            if SolarTerm.from_lunar_date(lunar_date).name == '立秋':
                li_qiu = lunar_date
            if not is_fu and (lunar_date - xia_zhi).days == 3:
                three_nine_days['初伏'] = curr_date
                is_fu = True
            if is_fu and (lunar_date - li_qiu).days == 0:
                three_nine_days['末伏'] = curr_date
                is_fu = False
            if is_fu:
                fu_count += 1
                if fu_count == 10:
                    three_nine_days['中伏'] = curr_date
                    fu_count = 0
            if not is_jiu and (lunar_date.month, lunar_date.day) == (12, 21) or (lunar_date.month, lunar_date.day) == (12, 22):
                three_nine_days['一九'] = curr_date
                is_jiu = True
                jiu_count = 1
            if is_jiu:
                jiu_count += 1
                if jiu_count == 10:
                    label = f'{jiu_count // 10}九'
                    three_nine_days[label] = curr_date
                    jiu_count = 0
                    if label == '九九':
                        break
            curr_date += date.resolution
        return three_nine_days

    @staticmethod
    def get_39label(date_obj: Union[date, LunarDate]) -> str:
        if isinstance(date_obj, date):
            date_obj = LunarDate.from_date(date_obj)
        three_nine_days = ThreeNineUtils.get_39days(date_obj.year)
        for label, three_nine_date in three_nine_days.items():
            if date_obj >= LunarDate.from_date(three_nine_date) and date_obj <= LunarDate.from_date(three_nine_date + date.resolution * 9):
                return label
        return ''

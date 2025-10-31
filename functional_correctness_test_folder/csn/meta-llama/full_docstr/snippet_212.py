
from datetime import date
from typing import Dict, Union
from lunardate import LunarDate


class ThreeNineUtils:
    '''三伏数九天工具函数
    '''
    @staticmethod
    def get_39days(year: int) -> Dict[str, date]:
        '''获取公历year年的三伏数九天对应的公历日期。
        '''
        # 计算入伏日期
        lunar_date = LunarDate(year, 7, 1)
        while lunar_date.lunar_day != 15 or lunar_date.lunar_month != 7:
            lunar_date = lunar_date + 1
        summer_begin = lunar_date + 6
        start_fu = summer_begin + \
            (summer_begin.lunar_day - 1) // 10 * 10 + 9 - summer_begin.lunar_day

        # 初伏、末伏、中伏
        chu_fu = start_fu.to_date()
        mo_fu = (start_fu + 29 if (start_fu + 29).lunar_month ==
                 7 else start_fu + 39).to_date()
        zhong_fu = (start_fu + 10).to_date()

        # 数九
        dong_zhi = LunarDate(year, 11, 1)
        while dong_zhi.lunar_month != 11 or dong_zhi.lunar_day != (21 if year % 4 == 3 else 22):
            dong_zhi = dong_zhi + 1
        shu_jiu = dong_zhi.to_date()

        return {
            '初伏': chu_fu,
            '中伏': zhong_fu,
            '末伏': mo_fu,
            '数九': shu_jiu,
        }

    @staticmethod
    def get_39label(date_obj: Union[date, LunarDate]) -> str:
        '''返回三伏数九天对应的标签，如果不是，返回空字符串。
        '''
        if isinstance(date_obj, date):
            date_obj = LunarDate.from_date(date_obj)

        year = date_obj.lunar_year
        fu_days = ThreeNineUtils.get_39days(year)
        jiu_days = fu_days.pop('数九')

        for label, fu_day in fu_days.items():
            if fu_day <= date_obj.to_date() < fu_day + (10 if label != '末伏' else 9 if (year - 1) % 4 == 3 else 10):
                return label

        if jiu_days <= date_obj.to_date() < jiu_days + 81:
            days = (date_obj.to_date() - jiu_days).days
            return f'{days // 9 + 1}九' + ('' if days % 9 == 0 else f'{days % 9}')

        return ''

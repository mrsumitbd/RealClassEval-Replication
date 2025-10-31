
from datetime import date
from typing import Dict, Union
from .. import LunarDate


class ThreeNineUtils:

    @staticmethod
    def get_39days(year: int) -> Dict[str, date]:
        '''获取公历year年的三伏数九天对应的公历日期。'''
        def get_solar_term_day(year, term):
            # Placeholder for actual implementation to get solar term day
            pass

        def get_xiaoshu_day(year):
            # Placeholder for actual implementation to get Xiaoshu day
            pass

        def get_dashu_day(year):
            # Placeholder for actual implementation to get Dashu day
            pass

        def get_liqiu_day(year):
            # Placeholder for actual implementation to get Liqiu day
            pass

        xiaoshu = get_xiaoshu_day(year)
        dashu = get_dashu_day(year)
        liqiu = get_liqiu_day(year)

        # Calculate Chufu (初伏), Zhongfu (中伏), Mofu (末伏)
        geng_days = []
        current_day = xiaoshu
        while len(geng_days) < 3:
            if current_day.weekday() == 5:  # Assuming Geng days are Saturdays (placeholder)
                geng_days.append(current_day)
            current_day += timedelta(days=1)

        chufu = geng_days[0]
        zhongfu = geng_days[1]
        mofu = geng_days[2]

        # Calculate 数九天 (Winter Solstice and following 81 days)
        dongzhi = get_solar_term_day(year, 'Dongzhi')
        shujiu_start = dongzhi
        shujiu_days = {
            '一九': shujiu_start,
            '二九': shujiu_start + timedelta(days=9),
            '三九': shujiu_start + timedelta(days=18),
            '四九': shujiu_start + timedelta(days=27),
            '五九': shujiu_start + timedelta(days=36),
            '六九': shujiu_start + timedelta(days=45),
            '七九': shujiu_start + timedelta(days=54),
            '八九': shujiu_start + timedelta(days=63),
            '九九': shujiu_start + timedelta(days=72),
        }

        return {
            '初伏': chufu,
            '中伏': zhongfu,
            '末伏': mofu,
            **shujiu_days
        }

    @staticmethod
    def get_39label(date_obj: Union[date, LunarDate]) -> str:
        if isinstance(date_obj, LunarDate):
            date_obj = date_obj.to_solar_date()

        year = date_obj.year
        days_dict = ThreeNineUtils.get_39days(year)

        # Check for 三伏 days
        for label, day in [('初伏', days_dict['初伏']),
                           ('中伏', days_dict['中伏']),
                           ('末伏', days_dict['末伏'])]:
            if date_obj == day:
                return label

        # Check for 数九 days
        dongzhi = days_dict['一九']
        delta = (date_obj - dongzhi).days
        if 0 <= delta < 81:
            period = (delta // 9) + 1
            if period <= 9:
                return f'{period}九'

        return ''

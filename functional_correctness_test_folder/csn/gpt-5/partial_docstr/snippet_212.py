from datetime import date, timedelta
from typing import Dict, Union, Any


class ThreeNineUtils:

    STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    CN_NUM = {1: '一', 2: '二', 3: '三', 4: '四',
              5: '五', 6: '六', 7: '七', 8: '八', 9: '九'}

    @staticmethod
    def _to_date(obj: Union[date, Any]) -> date:
        if isinstance(obj, date):
            return obj
        # Try common conversion methods for LunarDate-like objects
        for attr in ('to_date', 'to_solar_date', 'to_solar', 'solar_date'):
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                val = val() if callable(val) else val
                if isinstance(val, date):
                    return val
        # Try attributes year, month, day
        if all(hasattr(obj, x) for x in ('year', 'month', 'day')):
            return date(int(getattr(obj, 'year')), int(getattr(obj, 'month')), int(getattr(obj, 'day')))
        raise TypeError('Unsupported date object')

    @staticmethod
    def _sexagenary_day_index(d: date) -> int:
        # Assume 1984-02-02 is JiaZi (index 1)
        base = date(1984, 2, 2)
        offset = (d - base).days
        return (offset % 60) + 1

    @staticmethod
    def _is_geng_day(d: date) -> bool:
        idx = ThreeNineUtils._sexagenary_day_index(d)
        stem_index = ((idx - 1) % 10) + 1  # 1..10
        return stem_index == 7  # 庚

    @staticmethod
    def _first_geng_on_or_after(d: date) -> date:
        cur = d
        while not ThreeNineUtils._is_geng_day(cur):
            cur += timedelta(days=1)
        return cur

    @staticmethod
    def _nth_geng_on_or_after(d: date, n: int) -> date:
        count = 0
        cur = d
        while True:
            if ThreeNineUtils._is_geng_day(cur):
                count += 1
                if count == n:
                    return cur
            cur += timedelta(days=1)

    @staticmethod
    def _approx_summer_solstice(year: int) -> date:
        # Approximate 夏至 as June 21
        return date(year, 6, 21)

    @staticmethod
    def _approx_start_of_autumn(year: int) -> date:
        # Approximate 立秋 as August 7
        return date(year, 8, 7)

    @staticmethod
    def _approx_winter_solstice(year: int) -> date:
        # Approximate 冬至 as December 21
        return date(year, 12, 21)

    @staticmethod
    def get_39days(year: int) -> Dict[str, date]:
        # 三伏
        xiazhi = ThreeNineUtils._approx_summer_solstice(year)
        liqiu = ThreeNineUtils._approx_start_of_autumn(year)

        chu_fu = ThreeNineUtils._nth_geng_on_or_after(xiazhi, 3)
        zhong_fu = chu_fu + timedelta(days=10)
        mo_fu = ThreeNineUtils._first_geng_on_or_after(liqiu)

        res: Dict[str, date] = {
            '初伏': chu_fu,
            '中伏': zhong_fu,
            '末伏': mo_fu,
        }

        # 数九 starts from the 冬至 of this year
        dongzhi = ThreeNineUtils._approx_winter_solstice(year)
        for i in range(9):
            res[f'{ThreeNineUtils.CN_NUM[i + 1]}九'] = dongzhi + \
                timedelta(days=i * 9)

        return res

    @staticmethod
    def get_39label(date_obj: Union[date, Any]) -> str:
        d = ThreeNineUtils._to_date(date_obj)

        # 三伏 label
        daysinfo = ThreeNineUtils.get_39days(d.year)
        chu = daysinfo['初伏']
        zhong = daysinfo['中伏']
        mo = daysinfo['末伏']
        chu_end = zhong - timedelta(days=1)
        # 末伏 start is mo, ends after 10 days
        mo_end = mo + timedelta(days=9)
        # 中伏 ends the day before 末伏
        zhong_end = mo - timedelta(days=1)

        if chu <= d <= chu_end:
            return f'初伏第{(d - chu).days + 1}天'
        if zhong <= d <= zhong_end:
            return f'中伏第{(d - zhong).days + 1}天'
        if mo <= d <= mo_end:
            return f'末伏第{(d - mo).days + 1}天'

        # 数九 label: determine relevant 冬至 anchor
        dz_this = ThreeNineUtils._approx_winter_solstice(d.year)
        if d >= dz_this:
            anchor = dz_this
        else:
            anchor = ThreeNineUtils._approx_winter_solstice(d.year - 1)

        delta = (d - anchor).days
        if 0 <= delta <= 80:
            n = delta // 9 + 1
            day_in = delta % 9 + 1
            cn = ThreeNineUtils.CN_NUM.get(n, '')
            if cn:
                return f'{cn}九第{day_in}天'

        return ''


from datetime import date, timedelta
from typing import Dict, Union

try:
    from lunardate import LunarDate
except ImportError:
    class LunarDate:
        # Dummy class for type hinting if lunardate is not installed
        pass


class ThreeNineUtils:
    '''三伏数九天工具函数
    '''
    @staticmethod
    def get_39days(year: int) -> Dict[str, date]:
        '''获取公历year年的三伏数九天对应的公历日期。
        '''
        # Helper to get summer solstice and winter solstice
        # For simplicity, use approximate dates
        # 夏至: June 21, 冬至: December 21
        # 三伏天: 以夏至为基准
        # 数九天: 以冬至为基准

        # Find 夏至 (Summer Solstice)
        summer_solstice = date(year, 6, 21)
        # Find 冬至 (Winter Solstice)
        winter_solstice = date(year, 12, 21)

        # Find 初伏: 夏至后第3个庚日
        # Find 中伏: 初伏后第10天
        # Find 末伏: 中伏后第10天
        # 三伏天的长度：初伏10天，中伏10天，末伏10天（有时中伏为20天，视农历而定）

        # To get the "庚日", we need to calculate the Heavenly Stems for each day
        # The Heavenly Stems cycle every 10 days: 甲乙丙丁戊己庚辛壬癸
        # Let's assume 1984-02-02 is 甲子日, which is a known reference
        # We'll use this to calculate the stem for any date

        def get_ganzhi_index(d: date) -> int:
            # 1984-02-02 is 甲子日, Heavenly Stem index 0
            base = date(1984, 2, 2)
            delta = (d - base).days
            return delta % 10

        # Heavenly Stems: 甲(0), 乙(1), 丙(2), 丁(3), 戊(4), 己(5), 庚(6), 辛(7), 壬(8), 癸(9)
        # Find the first 庚日 (index 6) after 夏至
        first_geng = None
        d = summer_solstice
        while True:
            if get_ganzhi_index(d) == 6:
                first_geng = d
                break
            d += timedelta(days=1)
        # 初伏: 夏至后第3个庚日
        geng_count = 1
        geng_dates = [first_geng]
        d = first_geng + timedelta(days=1)
        while geng_count < 3:
            if get_ganzhi_index(d) == 6:
                geng_dates.append(d)
                geng_count += 1
            d += timedelta(days=1)
        chufu = geng_dates[2]  # 第3个庚日

        # 中伏: 初伏后第10天
        zhongfu = chufu + timedelta(days=10)
        # 末伏: 中伏后第10天
        # 但有时中伏为20天（闰月），我们用常规算法：末伏为立秋后第一个庚日
        # 立秋: 8月7日或8日
        liqiu = date(year, 8, 7)
        if liqiu.weekday() == 6:  # Sunday, 8月7日是立秋
            pass
        else:
            if date(year, 8, 8).weekday() == 6:
                liqiu = date(year, 8, 8)
        # 末伏: 立秋后第一个庚日
        d = liqiu
        while True:
            if get_ganzhi_index(d) == 6:
                mofu = d
                break
            d += timedelta(days=1)

        # 末伏长度10天
        mofu_end = mofu + timedelta(days=9)

        # 中伏长度: 末伏开始日 - 中伏开始日
        zhongfu_end = mofu - timedelta(days=1)

        # 数九天: 冬至起，每九天为一九，九个九
        shujio = {}
        for i in range(9):
            label = f"{i+1}九"
            start = winter_solstice + timedelta(days=i*9)
            shujio[label] = start

        return {
            "初伏": chufu,
            "中伏": zhongfu,
            "中伏结束": zhongfu_end,
            "末伏": mofu,
            "末伏结束": mofu_end,
            **shujio
        }

    @staticmethod
    def get_39label(date_obj: Union[date, 'LunarDate']) -> str:
        '''返回三伏数九天对应的标签，如果不是，返回空字符串。
        '''
        # If LunarDate, convert to date
        if hasattr(date_obj, 'toSolarDate'):
            d = date_obj.toSolarDate()
        else:
            d = date_obj

        year = d.year
        # For dates in January/February, 数九天可能属于上一年
        if d.month == 1 or (d.month == 2 and d.day < 28):
            # Check if date is before winter solstice
            if d < date(year, 2, 1):
                year -= 1

        days = ThreeNineUtils.get_39days(year)
        # 三伏天
        chufu = days["初伏"]
        zhongfu = days["中伏"]
        zhongfu_end = days["中伏结束"]
        mofu = days["末伏"]
        mofu_end = days["末伏结束"]

        if chufu <= d <= chufu + timedelta(days=9):
            idx = (d - chufu).days + 1
            return f"初伏第{idx}天"
        elif zhongfu <= d <= zhongfu_end:
            idx = (d - zhongfu).days + 1
            return f"中伏第{idx}天"
        elif mofu <= d <= mofu_end:
            idx = (d - mofu).days + 1
            return f"末伏第{idx}天"

        # 数九天
        for i in range(9):
            label = f"{i+1}九"
            start = days[label]
            end = start + timedelta(days=8)
            if start <= d <= end:
                idx = (d - start).days + 1
                return f"{label}第{idx}天"

        return ""

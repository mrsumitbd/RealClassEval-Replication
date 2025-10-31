from datetime import date, timedelta
from typing import Dict, Union

try:
    # pip install lunar-python
    from lunar_python import Solar
    _HAS_LUNAR = True
except Exception:
    _HAS_LUNAR = False

try:
    # optional: pip install lunardate
    from lunardate import LunarDate  # type: ignore
except Exception:
    class LunarDate:  # type: ignore
        pass


class ThreeNineUtils:
    '''三伏数九天工具函数
    '''
    @staticmethod
    def _ensure_dep():
        if not _HAS_LUNAR:
            raise RuntimeError(
                "lunar-python package is required for ThreeNineUtils")

    @staticmethod
    def _to_solar_date(date_obj: Union[date, LunarDate]) -> date:
        if isinstance(date_obj, date):
            return date_obj
        # handle lunardate.LunarDate if available
        if hasattr(date_obj, "toSolarDate") and callable(getattr(date_obj, "toSolarDate")):
            return date_obj.toSolarDate()  # type: ignore[attr-defined]
        # fallback: try attributes commonly present: year, month, day and a converter
        raise TypeError(
            "Unsupported date object type; expected datetime.date or lunardate.LunarDate")

    @staticmethod
    def _get_label_for_date(d: date) -> str:
        ThreeNineUtils._ensure_dep()
        s = Solar.fromYmd(d.year, d.month, d.day)
        l = s.getLunar()
        fu = l.getFu()
        if fu is not None:
            # 初伏/中伏/末伏 第n天
            name = fu.getName()  # 初伏/中伏/末伏
            idx = fu.getIndex()  # 1..10/20
            return f"{name}第{idx}天"
        sj = l.getShuJiu()
        if sj is not None:
            # 一九..九九 第n天
            name = sj.getName()  # 一九..九九
            idx = sj.getIndex()  # 1..9
            return f"{name}第{idx}天"
        return ""

    @staticmethod
    def get_39days(year: int) -> Dict[str, date]:
        '''获取公历year年的三伏数九天对应的公历日期。
        返回字典：键为标签（如“初伏第1天”、“一九第3天”），值为对应的公历日期。
        仅包含该公历年的日期。
        '''
        ThreeNineUtils._ensure_dep()
        start = date(year, 1, 1)
        end = date(year, 12, 31)
        res: Dict[str, date] = {}
        d = start
        one_day = timedelta(days=1)
        while d <= end:
            label = ThreeNineUtils._get_label_for_date(d)
            if label:
                res[label] = d
            d += one_day
        return res

    @staticmethod
    def get_39label(date_obj: Union[date, LunarDate]) -> str:
        '''返回三伏数九天对应的标签，如果不是，返回空字符串。
        '''
        d = ThreeNineUtils._to_solar_date(date_obj)
        return ThreeNineUtils._get_label_for_date(d)

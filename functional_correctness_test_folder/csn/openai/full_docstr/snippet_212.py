
from datetime import date, timedelta
from typing import Dict, Union

try:
    from lunardate import LunarDate
except ImportError as exc:
    raise ImportError(
        "The 'lunardate' package is required for ThreeNineUtils. "
        "Install it via pip: pip install lunardate"
    ) from exc


class ThreeNineUtils:
    """三伏数九天工具函数"""

    @staticmethod
    def _first_伏_start(year: int) -> date:
        """
        计算给定公历年份的三伏第一伏开始的公历日期。
        三伏第一伏开始于农历6月5日的第二天。
        """
        # 农历6月5日对应的公历日期

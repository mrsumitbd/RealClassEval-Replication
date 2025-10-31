import re
from typing import Union

class ChineseNumbers:
    RULES = [('一十', '十'), ('零[千百十]', '零'), ('零{2,}', '零'), ('零([亿|万])', '\\g<1>'), ('亿零{0,3}万', '亿'), ('零?_', '')]

    @staticmethod
    def measure_number(num: Union[int, str], upper: bool=False) -> str:
        """将数字转化为计量大/小写的中文数字，数字0的中文形式为“零”。

        >>> ChineseNumbers.measure_number(11)
        '十一'
        >>> ChineseNumbers.measure_number(204, True)
        '贰佰零肆'
        """
        if isinstance(num, str):
            _n = int(num)
        else:
            _n = num
        if _n < 0 or _n >= MAX_VALUE_LIMIT:
            raise ValueError('Out of range')
        num_str = str(num)
        capital_str = ''.join([LOWER_DIGITS[int(i)] for i in num_str])
        s_units = LOWER_UNITS[len(LOWER_UNITS) - len(num_str):]
        o = ''.join((f'{u}{d}' for u, d in zip(capital_str, s_units)))
        for p, d in ChineseNumbers.RULES:
            o = re.sub(p, d, o)
        if 10 <= _n < 20:
            o.replace('一十', '十')
        if upper:
            for _ld, _ud in zip(LOWER_DIGITS + LOWER_UNITS[:3], UPPER_DIGITS + UPPER_UNITS[:3]):
                o = o.replace(_ld, _ud)
        return o

    @staticmethod
    def order_number(num: Union[int, str], upper: bool=False) -> str:
        """将数字转化为编号大/小写的中文数字，数字0的中文形式为“〇”。

        >>> ChineseNumbers.order_number(1056)
        '一千〇五十六'
        """
        val = ChineseNumbers.measure_number(num, upper)
        ns = val.replace('零', '〇')
        return ns

    @staticmethod
    def to_chinese_number(num: Union[int, str], upper: bool=False, order: bool=False) -> str:
        """

        >>> ChineseNumbers.to_chinese_number(100000000)
        '一亿'
        >>> ChineseNumbers.to_chinese_number(204, upper=True)
        '贰佰零肆'
        >>> ChineseNumbers.to_chinese_number(204, upper=True, order=True)
        '贰佰〇肆'
        """
        if order:
            return ChineseNumbers.order_number(num, upper)
        else:
            return ChineseNumbers.measure_number(num, upper)
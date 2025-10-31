from dataclasses import dataclass

@dataclass
class SolarTime:
    """
    公历时间.
    """
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int

    def __str__(self):
        return f'{self.year}年{self.month}月{self.day}日{self.hour}时{self.minute}分{self.second}秒'

    def get_year(self):
        return self.year

    def get_month(self):
        return self.month

    def get_day(self):
        return self.day

    def get_hour(self):
        return self.hour

    def get_minute(self):
        return self.minute

    def get_second(self):
        return self.second
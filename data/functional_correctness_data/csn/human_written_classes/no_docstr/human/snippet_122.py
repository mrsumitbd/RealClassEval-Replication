class HijriDate:

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def weekday(self):
        for week in hijri.monthcalendar(self.year, self.month):
            for idx, day in enumerate(week):
                if day == self.day:
                    return idx
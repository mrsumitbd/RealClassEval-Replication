from datetime import date, datetime, timedelta
import calendar

class SCalendars:

    @staticmethod
    def get_last_day_of_this_month(year: int, month: int) -> date:
        return date(year, month, calendar.monthrange(year, month)[-1])

    @staticmethod
    def get_fist_day_of_year_week(year: int, week: int) -> date:
        fmt = f'{year}-W{week}-1'
        return datetime.strptime(fmt, '%Y-W%W-%w').date()
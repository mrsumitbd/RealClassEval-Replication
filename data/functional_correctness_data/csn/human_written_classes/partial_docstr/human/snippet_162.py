from dateparser.conf import settings
from dateparser.date import DateData

class CalendarBase:
    """Base setup class for non-Gregorian calendar system.

    :param source:
        Date string passed to calendar parser.
    :type source: str
    """
    parser = NotImplemented

    def __init__(self, source):
        self.source = source

    def get_date(self):
        try:
            date_obj, period = self.parser.parse(self.source, settings)
            return DateData(date_obj=date_obj, period=period)
        except ValueError:
            pass
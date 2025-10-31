
import datetime


class TimeUtils:
    """
    This is a time util class, including getting the current time and date, adding seconds to a datetime, converting between strings and datetime objects, calculating the time difference in minutes, and formatting a datetime object.
    """

    def __init__(self):
        """
        Get the current datetime
        """
        self.datetime = datetime.datetime.now()

    def get_current_time(self):
        """
        Return the current time in the format of '%H:%M:%S'
        :return: string
        """
        return self.datetime.strftime('%H:%M:%S')

    def get_current_date(self):
        """
        Return the current date in the format of "%Y-%m-%d"
        :return: string
        """
        return self.datetime.strftime('%Y-%m-%d')

    def add_seconds(self, seconds):
        """
        Add the specified number of seconds to the current time
        :param seconds: int, number of seconds to add
        :return: string, time after adding the specified number of seconds in the format '%H:%M:%S'
        """
        new_time = self.datetime + datetime.timedelta(seconds=seconds)
        return new_time.strftime('%H:%M:%S')

    def string_to_datetime(self, string):
        """
        Convert the time string to a datetime instance
        :param string: string, string before converting format
        :return: datetime instance
        """
        # Accepts "YYYY-M-D H:M:S"
        dt = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
        return dt

    def datetime_to_string(self, dt):
        """
        Convert a datetime instance to a string
        :param datetime: the datetime instance to convert
        :return: string, converted time string
        """
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def get_minutes(self, string_time1, string_time2):
        """
        Calculate how many minutes have passed between two times, and round the results to the nearest
        :return: int, the number of minutes between two times, rounded off
        """
        dt1 = datetime.datetime.strptime(string_time1, "%Y-%m-%d %H:%M:%S")
        dt2 = datetime.datetime.strptime(string_time2, "%Y-%m-%d %H:%M:%S")
        diff = abs((dt2 - dt1).total_seconds())
        return int(round(diff / 60))

    def get_format_time(self, year, month, day, hour, minute, second):
        """
        get format time
        :param year: int
        :param month: int
        :param day: int
        :param hour: int
        :param minute: int
        :param second: int
        :return: formatted time string
        """
        dt = datetime.datetime(year, month, day, hour, minute, second)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

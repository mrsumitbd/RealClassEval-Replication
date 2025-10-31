import cftime
import datetime

class DatetimeOffset:
    """A utility class for adding various time offsets to cftime datetimes.

    Parameters:
        unit (str): The unit of the time offset. Supported units are:
            - "YS" for years (start of the year)
            - "MS" for months (start of the month)
            - "W" for weeks
            - "D" for days
            - "H" for hours
            - "T" for minutes
            - "S" for seconds
        magnitude (int): The magnitude of the time offset.

    Methods:
        - `add_to_datetime(initial_dt: cftime.datetime) -> cftime.datetime`:
          Adds the specified time offset to the given cftime datetime and
          returns the resulting datetime.

    Attributes:
        - unit (str): The unit of the time offset.
        - magnitude (int): The magnitude of the time offset.
    """

    def __init__(self, unit, magnitude):
        supported_datetime_offsets = {'YS': add_year_start_offset_to_datetime, 'MS': add_month_start_offset_to_datetime, 'W': add_timedelta_fn(datetime.timedelta(weeks=1)), 'D': add_timedelta_fn(datetime.timedelta(days=1)), 'H': add_timedelta_fn(datetime.timedelta(hours=1)), 'T': add_timedelta_fn(datetime.timedelta(minutes=1)), 'S': add_timedelta_fn(datetime.timedelta(seconds=1))}
        if unit not in supported_datetime_offsets:
            raise ValueError(f'Unsupported datetime offset: {unit}. Supported offsets: YS, MS, W, D, H, T, S')
        self.unit = unit
        self.magnitude = magnitude
        self._add_offset_to_datetime = supported_datetime_offsets[unit]

    def add_to_datetime(self, initial_dt):
        """Takes an initial cftime datetime,
        and returns a datetime with the offset added"""
        if not isinstance(initial_dt, cftime.datetime):
            raise TypeError(f'Invalid initial datetime type: {type(initial_dt)}. Expected type: cftime.datetime')
        return self._add_offset_to_datetime(initial_dt=initial_dt, n=self.magnitude)
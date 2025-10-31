import datetime
import pytz

class DateTime:

    @staticmethod
    def parse(date_str):
        if not isinstance(date_str, str):
            return
        try:
            return datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        except Exception:
            raise ValueError('dates must be ISO 8601 date format YYYY-MM-DDThh:mm:ss.sssZ')

    @staticmethod
    def iso8601(dt):
        return dt.replace(microsecond=0).strftime('%Y-%m-%dT%H:%M:%S') + '.%03dZ' % (dt.microsecond // 1000)

    @staticmethod
    def localtime(dt, timezone=None, fmt='%Y/%m/%d %H:%M:%S'):
        tz = pytz.timezone(timezone)
        try:
            return dt.replace(tzinfo=pytz.UTC).astimezone(tz).strftime(fmt)
        except AttributeError:
            return
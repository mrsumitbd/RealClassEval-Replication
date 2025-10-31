import time
import os
import locale
import subprocess


class SystemTimeDetector:
    '''System timezone and time format detection.'''

    @staticmethod
    def get_timezone() -> str:
        '''Detect system timezone.'''
        # Try time.tzname
        try:
            if time.daylight and time.localtime().tm_isdst:
                return time.tzname[1]
            else:
                return time.tzname[0]
        except Exception:
            pass
        # Try /etc/timezone (Linux)
        try:
            if os.path.exists('/etc/timezone'):
                with open('/etc/timezone') as f:
                    return f.read().strip()
        except Exception:
            pass
        # Try timedatectl (Linux)
        try:
            output = subprocess.check_output(
                ['timedatectl'], stderr=subprocess.DEVNULL, encoding='utf-8')
            for line in output.splitlines():
                if 'Time zone:' in line:
                    return line.split('Time zone:')[1].split()[0]
        except Exception:
            pass
        # Try TZ env
        tz = os.environ.get('TZ')
        if tz:
            return tz
        return 'Unknown'

    @staticmethod
    def get_time_format() -> str:
        '''Detect system time format ('12h' or '24h').'''
        try:
            locale.setlocale(locale.LC_TIME, '')
        except Exception:
            pass
        try:
            fmt = locale.nl_langinfo(locale.T_FMT)
        except AttributeError:
            # Fallback for Windows
            fmt = time.strftime('%X')
        # Check for %I (12-hour) or %H (24-hour)
        if '%I' in fmt or 'I' in fmt:
            return '12h'
        if '%H' in fmt or 'H' in fmt:
            return '24h'
        # Fallback: check sample time string
        sample = time.strftime(fmt, time.strptime('13:00', '%H:%M'))
        if '13' in sample:
            return '24h'
        if '01' in sample or 'PM' in sample or 'AM' in sample:
            return '12h'
        return '24h'

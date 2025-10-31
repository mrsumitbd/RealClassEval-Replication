import platform
import contextlib
from typing import Any, Dict, List, Optional, Set, Union
import os
import subprocess

class SystemTimeDetector:
    """System timezone and time format detection."""

    @staticmethod
    def get_timezone() -> str:
        """Detect system timezone."""
        tz: Optional[str] = os.environ.get('TZ')
        if tz:
            return tz
        system: str = platform.system()
        if system == 'Darwin':
            try:
                readlink_result: subprocess.CompletedProcess[str] = subprocess.run(['readlink', '/etc/localtime'], capture_output=True, text=True, check=True)
                tz_path: str = readlink_result.stdout.strip()
                if 'zoneinfo/' in tz_path:
                    return tz_path.split('zoneinfo/')[-1]
            except Exception:
                pass
        elif system == 'Linux':
            if os.path.exists('/etc/timezone'):
                try:
                    with open('/etc/timezone') as f:
                        tz_content: str = f.read().strip()
                        if tz_content:
                            return tz_content
                except Exception:
                    pass
            try:
                timedatectl_result: subprocess.CompletedProcess[str] = subprocess.run(['timedatectl', 'show', '-p', 'Timezone', '--value'], capture_output=True, text=True, check=True)
                tz_result: str = timedatectl_result.stdout.strip()
                if tz_result:
                    return tz_result
            except Exception:
                pass
        elif system == 'Windows':
            with contextlib.suppress(Exception):
                tzutil_result: subprocess.CompletedProcess[str] = subprocess.run(['tzutil', '/g'], capture_output=True, text=True, check=True)
                return tzutil_result.stdout.strip()
        return 'UTC'

    @staticmethod
    def get_time_format() -> str:
        """Detect system time format ('12h' or '24h')."""
        return TimeFormatDetector.detect_from_system()
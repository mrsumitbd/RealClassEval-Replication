import re
import sys

class WifiManager:
    """
    Simulates Android WifiManager.

    @see: http://developer.android.com/reference/android/net/wifi/WifiManager.html
    """
    WIFI_STATE_DISABLING = 0
    WIFI_STATE_DISABLED = 1
    WIFI_STATE_ENABLING = 2
    WIFI_STATE_ENABLED = 3
    WIFI_STATE_UNKNOWN = 4
    WIFI_IS_ENABLED_RE = re.compile('Wi-Fi is enabled')
    WIFI_IS_DISABLED_RE = re.compile('Wi-Fi is disabled')

    def __init__(self, device):
        """
        Constructor.
        :param device:
        :type device:
        """
        self.device = device

    def getWifiState(self):
        """
        Gets the Wi-Fi enabled state.

        @return: One of WIFI_STATE_DISABLED, WIFI_STATE_DISABLING, WIFI_STATE_ENABLED, WIFI_STATE_ENABLING, WIFI_STATE_UNKNOWN
        """
        result = self.device.shell('dumpsys wifi')
        if result:
            state = result.splitlines()[0]
            if self.WIFI_IS_ENABLED_RE.match(state):
                return self.WIFI_STATE_ENABLED
            elif self.WIFI_IS_DISABLED_RE.match(state):
                return self.WIFI_STATE_DISABLED
        print('UNKNOWN WIFI STATE:', state, file=sys.stderr)
        return self.WIFI_STATE_UNKNOWN

class WifiManager:
    '''
    Simulates Android WifiManager.
    @see: http://developer.android.com/reference/android/net/wifi/WifiManager.html
    '''
    WIFI_STATE_DISABLED = 1
    WIFI_STATE_DISABLING = 0
    WIFI_STATE_ENABLED = 3
    WIFI_STATE_ENABLING = 2
    WIFI_STATE_UNKNOWN = 4

    def __init__(self, device):
        self.device = device
        # Simulate wifi state, default to enabled
        self._wifi_state = WifiManager.WIFI_STATE_ENABLED

    def getWifiState(self):
        return self._wifi_state

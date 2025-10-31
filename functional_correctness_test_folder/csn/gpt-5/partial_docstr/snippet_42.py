class WifiManager:
    '''
    Simulates Android WifiManager.
    @see: http://developer.android.com/reference/android/net/wifi/WifiManager.html
    '''
    # Wi-Fi state constants (mirroring Android WifiManager)
    WIFI_STATE_DISABLING = 0
    WIFI_STATE_DISABLED = 1
    WIFI_STATE_ENABLING = 2
    WIFI_STATE_ENABLED = 3
    WIFI_STATE_UNKNOWN = 4

    def __init__(self, device):
        self._device = device
        self._state = getattr(device, "wifi_state", self.WIFI_STATE_UNKNOWN)

    def getWifiState(self):
        return self._state

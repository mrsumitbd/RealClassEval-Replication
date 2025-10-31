
class WifiManager:
    '''
    Simulates Android WifiManager.
    @see: http://developer.android.com/reference/android/net/wifi/WifiManager.html
    '''

    def __init__(self, device):
        self.device = device
        # Assuming 0 means WIFI_STATE_DISABLED, 1 means WIFI_STATE_ENABLED, etc.
        self.wifi_state = 0

    def getWifiState(self):
        return self.wifi_state

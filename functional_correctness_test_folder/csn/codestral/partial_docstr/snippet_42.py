
class WifiManager:
    '''
    Simulates Android WifiManager.
    @see: http://developer.android.com/reference/android/net/wifi/WifiManager.html
    '''

    def __init__(self, device):
        self.device = device
        self.wifi_state = "WIFI_STATE_DISABLED"

    def getWifiState(self):
        return self.wifi_state

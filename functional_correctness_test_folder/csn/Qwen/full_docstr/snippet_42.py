
class WifiManager:
    '''
    Simulates Android WifiManager.
    @see: http://developer.android.com/reference/android/net/wifi/WifiManager.html
    '''

    WIFI_STATE_DISABLED = 0
    WIFI_STATE_DISABLING = 1
    WIFI_STATE_ENABLED = 2
    WIFI_STATE_ENABLING = 3
    WIFI_STATE_UNKNOWN = 4

    def __init__(self, device):
        '''
        Constructor.
        :param device:
        :type device:
        '''
        self.device = device
        self.wifi_state = self.WIFI_STATE_UNKNOWN

    def getWifiState(self):
        '''
        Gets the Wi-Fi enabled state.
        @return: One of WIFI_STATE_DISABLED, WIFI_STATE_DISABLING, WIFI_STATE_ENABLED, WIFI_STATE_ENABLING, WIFI_STATE_UNKNOWN
        '''
        return self.wifi_state

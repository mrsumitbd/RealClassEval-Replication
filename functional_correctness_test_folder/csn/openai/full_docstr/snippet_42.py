
class WifiManager:
    '''
    Simulates Android WifiManager.
    @see: http://developer.android.com/reference/android/net/wifi/WifiManager.html
    '''

    # Wi‑Fi state constants
    WIFI_STATE_DISABLED = 0
    WIFI_STATE_DISABLING = 1
    WIFI_STATE_ENABLED = 2
    WIFI_STATE_ENABLING = 3
    WIFI_STATE_UNKNOWN = 4

    def __init__(self, device):
        '''
        Constructor.
        :param device: An object representing the device. It may expose a
                       `wifi_state` attribute or a boolean `wifi_enabled`
                       attribute.
        :type device:
        '''
        self.device = device

    def getWifiState(self):
        '''
        Gets the Wi‑Fi enabled state.
        @return: One of WIFI_STATE_DISABLED, WIFI_STATE_DISABLING,
                 WIFI_STATE_ENABLED, WIFI_STATE_ENABLING, WIFI_STATE_UNKNOWN
        '''
        # Prefer an explicit state if the device provides it
        if hasattr(self.device, 'wifi_state'):
            state = getattr(self.device, 'wifi_state')
            if state in (
                self.WIFI_STATE_DISABLED,
                self.WIFI_STATE_DISABLING,
                self.WIFI_STATE_ENABLED,
                self.WIFI_STATE_ENABLING,
            ):
                return state

        # Fallback: interpret a boolean `wifi_enabled` attribute
        if hasattr(self.device, 'wifi_enabled'):
            return (
                self.WIFI_STATE_ENABLED
                if getattr(self.device, 'wifi_enabled')
                else self.WIFI_STATE_DISABLED
            )

        # If nothing is available, return UNKNOWN
        return self.WIFI_STATE_UNKNOWN


from enum import Enum


class WifiState(Enum):
    WIFI_STATE_DISABLED = 1
    WIFI_STATE_DISABLING = 2
    WIFI_STATE_ENABLED = 3
    WIFI_STATE_ENABLING = 4
    WIFI_STATE_UNKNOWN = 5


class WifiManager:
    '''
    Simulates Android WifiManager.
    @see: http://developer.android.com/reference/android/net/wifi/WifiManager.html
    '''

    def __init__(self, device):
        '''
        Constructor.
        :param device:
        :type device:
        '''
        self.device = device
        self.wifi_state = WifiState.WIFI_STATE_UNKNOWN

    def getWifiState(self):
        '''
        Gets the Wi-Fi enabled state.
        @return: One of WIFI_STATE_DISABLED, WIFI_STATE_DISABLING, WIFI_STATE_ENABLED, WIFI_STATE_ENABLING, WIFI_STATE_UNKNOWN
        '''
        # For simulation purposes, assume we can get the wifi state from the device
        # In a real implementation, you would use the device's API to get the wifi state
        # For example, using ADB commands or a library that interacts with the device
        # Here, we just return a static value for demonstration purposes
        return self.wifi_state


# Example usage:
if __name__ == "__main__":
    class Device:
        pass

    device = Device()
    wifi_manager = WifiManager(device)
    wifi_manager.wifi_state = WifiState.WIFI_STATE_ENABLED
    print(wifi_manager.getWifiState())

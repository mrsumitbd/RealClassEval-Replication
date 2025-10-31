
class WifiManager:
    """
    Simulates Android WifiManager.
    @see: http://developer.android.com/reference/android/net/wifi/WifiManager.html
    """

    # Wifi state constants (Android values)
    WIFI_STATE_UNKNOWN = -1
    WIFI_STATE_DISABLED = 0
    WIFI_STATE_DISABLING = 1
    WIFI_STATE_ENABLED = 3
    WIFI_STATE_ENABLING = 2

    def __init__(self, device):
        """
        Initialize the WifiManager with a device object.

        The device is expected to expose either:
          * a boolean attribute `wifi_enabled`
          * an integer attribute `wifi_state` matching one of the constants above
        """
        self.device = device

    def getWifiState(self):
        """
        Return the current Wi-Fi state of the device.

        If the device provides a `wifi_state` attribute, that value is returned.
        Otherwise, if the device provides a boolean `wifi_enabled` attribute,
        the corresponding state constant is returned.
        If neither attribute is present, WIFI_STATE_UNKNOWN is returned.
        """
        # Prefer explicit state if available
        if hasattr(self.device, "wifi_state"):
            state = getattr(self.device, "wifi_state")
            if isinstance(state, int):
                return state

        # Fallback to boolean enabled flag
        if hasattr(self.device, "wifi_enabled"):
            enabled = getattr(self.device, "wifi_enabled")
            if isinstance(enabled, bool):
                return self.WIFI_STATE_ENABLED if enabled else self.WIFI_STATE_DISABLED

        # Unknown state
        return self.WIFI_STATE_UNKNOWN

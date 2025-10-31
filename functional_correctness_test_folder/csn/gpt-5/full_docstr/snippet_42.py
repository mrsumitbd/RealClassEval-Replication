class WifiManager:
    '''
    Simulates Android WifiManager.
    @see: http://developer.android.com/reference/android/net/wifi/WifiManager.html
    '''

    WIFI_STATE_DISABLING = 0
    WIFI_STATE_DISABLED = 1
    WIFI_STATE_ENABLING = 2
    WIFI_STATE_ENABLED = 3
    WIFI_STATE_UNKNOWN = 4

    def __init__(self, device):
        '''
        Constructor.
        :param device:
        :type device:
        '''
        self.device = device

    def _normalize_state(self, value):
        if value is None:
            return self.WIFI_STATE_UNKNOWN

        # Numeric direct mapping
        try:
            ivalue = int(value)
            if ivalue in {
                self.WIFI_STATE_DISABLED,
                self.WIFI_STATE_DISABLING,
                self.WIFI_STATE_ENABLED,
                self.WIFI_STATE_ENABLING,
                self.WIFI_STATE_UNKNOWN,
            }:
                return ivalue
        except (ValueError, TypeError):
            pass

        # Boolean-like
        if isinstance(value, bool):
            return self.WIFI_STATE_ENABLED if value else self.WIFI_STATE_DISABLED

        # String mapping
        sval = str(value).strip().lower()
        mapping = {
            "0": self.WIFI_STATE_DISABLED,
            "1": self.WIFI_STATE_ENABLED,
            "enabled": self.WIFI_STATE_ENABLED,
            "disabled": self.WIFI_STATE_DISABLED,
            "enabling": self.WIFI_STATE_ENABLING,
            "disabling": self.WIFI_STATE_DISABLING,
            "unknown": self.WIFI_STATE_UNKNOWN,
            "on": self.WIFI_STATE_ENABLED,
            "off": self.WIFI_STATE_DISABLED,
            "true": self.WIFI_STATE_ENABLED,
            "false": self.WIFI_STATE_DISABLED,
        }
        return mapping.get(sval, self.WIFI_STATE_UNKNOWN)

    def getWifiState(self):
        '''
        Gets the Wi-Fi enabled state.
        @return: One of WIFI_STATE_DISABLED, WIFI_STATE_DISABLING, WIFI_STATE_ENABLED, WIFI_STATE_ENABLING, WIFI_STATE_UNKNOWN
        '''
        # Prefer explicit method if available
        if hasattr(self.device, "get_wifi_state") and callable(getattr(self.device, "get_wifi_state")):
            try:
                return self._normalize_state(self.device.get_wifi_state())
            except Exception:
                pass

        # Boolean query methods
        if hasattr(self.device, "is_wifi_enabled") and callable(getattr(self.device, "is_wifi_enabled")):
            try:
                return self._normalize_state(self.device.is_wifi_enabled())
            except Exception:
                pass

        # Attributes commonly used
        for attr in ("wifi_state", "wifiEnabled", "wifi_enabled", "wifiState"):
            if hasattr(self.device, attr):
                try:
                    return self._normalize_state(getattr(self.device, attr))
                except Exception:
                    pass

        # Shell-based query if device exposes a shell method
        # Try Android settings get global wifi_on (returns "1" or "0")
        if hasattr(self.device, "shell") and callable(getattr(self.device, "shell")):
            try:
                out = self.device.shell("settings get global wifi_on")
                if out is not None:
                    return self._normalize_state(str(out).strip())
            except Exception:
                pass
            # Fallback to svc wifi (some implementations may return status text)
            try:
                out = self.device.shell("svc wifi status")
                if out:
                    text = str(out).lower()
                    if "enabled" in text or "on" in text:
                        return self.WIFI_STATE_ENABLED
                    if "disabled" in text or "off" in text:
                        return self.WIFI_STATE_DISABLED
            except Exception:
                pass

        return self.WIFI_STATE_UNKNOWN

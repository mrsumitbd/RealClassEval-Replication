class WifiManager:
    def __init__(self, device):
        self._device = device
        self._last_state = None

    def _normalize_state(self, value):
        if value is None:
            return "unknown"

        if isinstance(value, bool):
            return "enabled" if value else "disabled"

        try:
            # Handle integers like 1/0
            if isinstance(value, (int, float)):
                return "enabled" if value != 0 else "disabled"
        except Exception:
            pass

        s = str(value).strip().lower()

        truthy = {"on", "enabled", "enable", "true",
                  "1", "up", "connected", "available"}
        falsy = {"off", "disabled", "disable", "false",
                 "0", "down", "disconnected", "unavailable"}

        if s in truthy:
            return "enabled"
        if s in falsy:
            return "disabled"

        return "unknown"

    def _get_from_attr_or_call(self, obj, names):
        for name in names:
            if hasattr(obj, name):
                attr = getattr(obj, name)
                try:
                    if callable(attr):
                        return attr()
                    return attr
                except Exception:
                    continue
        return None

    def getWifiState(self):
        dev = self._device

        # 1) Common method names that may directly provide state
        value = self._get_from_attr_or_call(dev, [
            "get_wifi_state",
            "getWifiState",
            "wifi_state",
            "wifiState",
        ])
        if value is not None:
            state = self._normalize_state(value)
            self._last_state = state
            return state

        # 2) Common boolean/flag attributes
        for name in ["wifi_enabled", "wifiEnabled", "is_wifi_enabled", "isWifiEnabled", "wifiOn", "wifi_on"]:
            if hasattr(dev, name):
                val = getattr(dev, name)
                state = self._normalize_state(val)
                self._last_state = state
                return state

        # 3) Nested wifi object with state/enabled
        if hasattr(dev, "wifi"):
            wifi = getattr(dev, "wifi")
            value = self._get_from_attr_or_call(wifi, [
                "state",
                "get_state",
                "getState",
                "enabled",
                "is_enabled",
                "isEnabled",
            ])
            if value is not None:
                state = self._normalize_state(value)
                self._last_state = state
                return state

        # 4) Network interface like signals (best-effort)
        for name in ["network", "net", "radio"]:
            if hasattr(dev, name):
                obj = getattr(dev, name)
                value = self._get_from_attr_or_call(obj, [
                    "wifi_state",
                    "get_wifi_state",
                    "wifiEnabled",
                    "is_wifi_enabled",
                ])
                if value is not None:
                    state = self._normalize_state(value)
                    self._last_state = state
                    return state

        # 5) Fallback to last known or unknown
        return self._last_state or "unknown"

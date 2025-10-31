class WifiManager:
    def __init__(self, device):
        self.device = device

    def getWifiState(self):
        if isinstance(self.device, dict):
            return self.device.get("wifi_state")
        return getattr(self.device, "wifi_state", None)

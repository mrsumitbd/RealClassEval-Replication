
class WifiManager:

    def __init__(self, device):
        self.device = device
        # Simulate wifi state: True for ON, False for OFF
        self._wifi_state = False

    def getWifiState(self):
        return "ON" if self._wifi_state else "OFF"

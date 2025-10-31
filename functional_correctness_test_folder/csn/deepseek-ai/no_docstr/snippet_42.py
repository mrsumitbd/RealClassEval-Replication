
class WifiManager:

    def __init__(self, device):
        self.device = device
        self.wifi_state = False

    def getWifiState(self):
        return self.wifi_state


class WifiManager:

    def __init__(self, device):
        self.device = device
        self.wifi_state = False  # Assuming False means WiFi is off and True means WiFi is on

    def getWifiState(self):
        return self.wifi_state

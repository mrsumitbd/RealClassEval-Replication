
class WifiManager:

    def __init__(self, device):

        self.device = device

    def getWifiState(self):

        return self.device.get_wifi_state()


class WifiManager:

    def __init__(self, device):
        """
        Initialize the WifiManager class.

        Args:
            device (object): The device object that provides wifi functionality.
        """
        self.device = device
        self.wifi_state = None

    def getWifiState(self):
        """
        Get the current state of the wifi.

        Returns:
            str: The current wifi state.
        """
        # Assuming the device object has a method to get the wifi state
        self.wifi_state = self.device.get_wifi_state()
        return self.wifi_state


# Example usage:

class Device:
    def __init__(self):
        self.wifi_state = "DISABLED"

    def get_wifi_state(self):
        return self.wifi_state

    def enable_wifi(self):
        self.wifi_state = "ENABLED"

    def disable_wifi(self):
        self.wifi_state = "DISABLED"


def main():
    device = Device()
    wifi_manager = WifiManager(device)
    print(wifi_manager.getWifiState())  # Output: DISABLED
    device.enable_wifi()
    print(wifi_manager.getWifiState())  # Output: ENABLED


if __name__ == "__main__":
    main()

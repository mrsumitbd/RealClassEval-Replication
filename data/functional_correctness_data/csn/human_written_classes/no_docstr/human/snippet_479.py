import dataclasses
from typing import List, Optional, Iterable, Dict, Any, Union

@dataclasses.dataclass
class WLanSettings:
    index: int
    enabled: bool
    ssid: str
    mac: Optional[str]
    broadcast: bool
    auth_mode: str
    id: Optional[str]
    radius_key: Optional[str]
    wpa_encryption_modes: str
    wep_key_index: int
    guest_off_time: int
    is_guest_network: bool

    @classmethod
    def from_dict(cls, data: dict) -> 'WLanSettings':
        return WLanSettings(index=int(data.get('Index', 0)), enabled=data.get('WifiEnable') == '1', ssid=data.get('WifiSsid', ''), mac=data.get('WifiMac'), broadcast=data.get('WifiBroadcast') == '1', auth_mode=data.get('WifiAuthmode', ''), wpa_encryption_modes=data.get('WifiWpaencryptionmodes', ''), wep_key_index=int(data.get('WifiWepKeyIndex', 0)), guest_off_time=int(data.get('wifiguestofftime', 0)), is_guest_network=data.get('wifiisguestnetwork', '0') == '1', id=data.get('ID'), radius_key=data.get('WifiRadiusKey'))

    def to_dict(self) -> dict:
        return {'Index': str(self.index), 'WifiEnable': '1' if self.enabled else '0', 'WifiSsid': self.ssid, 'WifiMac': self.mac, 'WifiBroadcast': '1' if self.broadcast else '0', 'WifiAuthmode': self.auth_mode, 'WifiWpaencryptionmodes': self.wpa_encryption_modes, 'WifiWepKeyIndex': str(self.wep_key_index), 'wifiguestofftime': str(self.guest_off_time)}
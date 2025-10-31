import struct
from typing import Tuple
import typing

class EtherFrame:
    __slots__ = ['source_mac', 'target_mac', 'ether_type', 'vlan_id', 'tpid']

    def __init__(self, source_mac: bytes, target_mac: bytes, ether_type: int, vlan_id: typing.Optional[int]=None, tpid: typing.Optional[int]=None):
        self.source_mac = source_mac
        self.target_mac = target_mac
        self.ether_type = ether_type
        self.vlan_id = vlan_id
        self.tpid = tpid

    def encode(self) -> bytes:
        if self.vlan_id is None:
            return struct.pack('6s6sH', *(getattr(self, slot) for slot in self.__slots__[:-2]))
        return struct.pack('6s6sHHH', *(getattr(self, slot) for slot in self.__slots__))

    @classmethod
    def decode(cls, packet: bytes) -> Tuple['EtherFrame', bytes]:
        vlan_id = None
        tpid = None
        if struct.unpack(f'!H', packet[12:14])[0] == Layer2.VLAN.value:
            target_mac, source_mac, tpid, vlan_id, ether_type, data = struct.unpack(f'!6s6sHHH{len(packet) - ETHER_HEADER_LEN - VLAN_HEADER_LEN}s', packet)
        else:
            target_mac, source_mac, ether_type, data = struct.unpack(f'!6s6sH{len(packet) - ETHER_HEADER_LEN}s', packet)
        return (cls(source_mac, target_mac, ether_type, vlan_id, tpid), data)

    def debug(self) -> str:
        if self.vlan_id is None:
            return f'EtherFrame(source={pretty_mac(self.source_mac)}, target={pretty_mac(self.target_mac)}, ether_type={Layer2(self.ether_type).name})'
        return f'EtherFrame(source={pretty_mac(self.source_mac)}, target={pretty_mac(self.target_mac)}, ether_type={Layer2(self.ether_type).name}, vlan={self.vlan_id})'
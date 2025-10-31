from typing import List, Dict, Optional, Tuple, Any

class PortInfo:
    """Information about a port and its usage"""

    def __init__(self, port: int, protocol: str='tcp', pid: Optional[int]=None, process_name: Optional[str]=None, address: str='0.0.0.0'):
        self.port = port
        self.protocol = protocol.lower()
        self.pid = pid
        self.process_name = process_name
        self.address = address

    def __str__(self) -> str:
        if self.process_name and self.pid:
            return f'{self.address}:{self.port}/{self.protocol} - {self.process_name} (PID: {self.pid})'
        return f'{self.address}:{self.port}/{self.protocol}'

    def to_dict(self) -> Dict[str, Any]:
        return {'port': self.port, 'protocol': self.protocol, 'pid': self.pid, 'process_name': self.process_name, 'address': self.address}
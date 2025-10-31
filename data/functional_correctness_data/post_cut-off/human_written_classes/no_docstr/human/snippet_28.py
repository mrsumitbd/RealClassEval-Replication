import os
import ray
import socket
from typing import Tuple

class WorkerHelper:

    def _get_node_ip(self) -> str:
        host_ipv4 = os.getenv('MY_HOST_IP', None)
        host_ipv6 = os.getenv('MY_HOST_IPV6', None)
        host_ip_by_env = host_ipv4 or host_ipv6
        host_ip_by_sdk = ray._private.services.get_node_ip_address()
        host_ip = host_ip_by_env or host_ip_by_sdk
        return host_ip

    def _get_free_port(self) -> int:
        with socket.socket() as sock:
            sock.bind(('', 0))
            return sock.getsockname()[1]

    def get_availale_master_addr_port(self) -> Tuple[str, str]:
        return (self._get_node_ip(), str(self._get_free_port()))

    def _get_pid(self):
        return
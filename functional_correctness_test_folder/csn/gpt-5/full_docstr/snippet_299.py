import socket
from urllib.parse import urlparse
from typing import Any, Dict, Iterable, Optional, Set, Tuple, Union


class _AddressListener:
    '''Listener for new addresses of interest.'''

    def __init__(self, subscriber, services: Union[str, Iterable[str]] = '', nameserver: str = 'localhost'):
        '''Initialize address listener.'''
        self._subscriber = subscriber
        self._services: Set[str] = self._normalize_services(services)
        self._nameserver = nameserver

    def handle_msg(self, msg):
        '''Handle the message *msg*.'''
        parsed = self._parse_msg(msg)
        if not parsed:
            return

        service = (parsed.get('service') or '').lower() or None
        if self._services and service and service not in self._services:
            return
        if self._services and not service:
            return

        host = parsed.get('address') or parsed.get('host')
        if not host:
            return

        port = parsed.get('port')
        meta = parsed.get('metadata') or parsed.get('meta') or {}

        result = {
            'service': service,
            'host': host,
            'port': port,
            'metadata': meta,
        }

        resolved = self._resolve_addresses(host, port)
        if resolved:
            result['addresses'] = [ip for ip, _ in resolved]
            result['sockaddrs'] = [sa for _, sa in resolved]
        else:
            result['addresses'] = []
            result['sockaddrs'] = []

        self._notify(result)

    # Internal helpers

    def _notify(self, payload: Dict[str, Any]) -> None:
        target = self._subscriber
        if hasattr(target, 'on_address') and callable(getattr(target, 'on_address')):
            target.on_address(payload)
            return
        if hasattr(target, 'notify') and callable(getattr(target, 'notify')):
            target.notify(payload)
            return
        if callable(target):
            target(payload)
            return
        raise TypeError(
            'Subscriber is not callable and lacks on_address/notify methods')

    def _normalize_services(self, services: Union[str, Iterable[str]]) -> Set[str]:
        if services is None:
            return set()
        if isinstance(services, str):
            s = services.strip()
            if not s:
                return set()
            parts = [p.strip().lower()
                     for p in s.replace(',', ' ').split() if p.strip()]
            return set(parts)
        try:
            return {str(s).strip().lower() for s in services if str(s).strip()}
        except TypeError:
            return {str(services).strip().lower()} if str(services).strip() else set()

    def _parse_msg(self, msg: Any) -> Optional[Dict[str, Any]]:
        if msg is None:
            return None

        if isinstance(msg, dict):
            return dict(msg)

        if isinstance(msg, (list, tuple)):
            if len(msg) == 3:
                service, host, port = msg
                return {'service': str(service) if service is not None else None,
                        'address': str(host),
                        'port': int(port) if port is not None else None}
            if len(msg) == 2:
                service, host = msg
                return {'service': str(service) if service is not None else None,
                        'address': str(host)}
            if len(msg) == 1:
                return self._parse_msg(msg[0])
            return None

        if isinstance(msg, str):
            s = msg.strip()
            if not s:
                return None
            parsed = urlparse(s)
            if parsed.scheme and (parsed.netloc or parsed.path):
                host = parsed.hostname or parsed.path or ''
                port = parsed.port
                return {'service': parsed.scheme.lower(),
                        'address': host,
                        'port': port}
            parts = s.replace('://', ' ').split()
            if len(parts) == 3:
                service, host, port = parts
                try:
                    port = int(port)
                except ValueError:
                    port = None
                return {'service': service.lower(), 'address': host, 'port': port}
            if len(parts) == 2:
                a, b = parts
                # Heuristic: if b is int-like, then (host, port); otherwise (service, host)
                try:
                    port = int(b)
                    return {'service': None, 'address': a, 'port': port}
                except ValueError:
                    return {'service': a.lower(), 'address': b}
            if len(parts) == 1:
                return {'service': None, 'address': parts[0]}
            return None

        # Fallback to string conversion
        return self._parse_msg(str(msg))

    def _resolve_addresses(self, host: str, port: Optional[int]) -> Optional[list]:
        try:
            # getaddrinfo will use system resolver; nameserver hint is stored but not enforced
            # We attempt both stream and datagram for broader coverage
            infos = []
            for socktype in (socket.SOCK_STREAM, socket.SOCK_DGRAM):
                try:
                    gai = socket.getaddrinfo(
                        host, port or 0, socket.AF_UNSPEC, socktype)
                    for family, stype, proto, _canon, sockaddr in gai:
                        ip = sockaddr[0]
                        infos.append((ip, sockaddr))
                except socket.gaierror:
                    continue
            # Deduplicate by sockaddr
            seen = set()
            unique = []
            for ip, sa in infos:
                key = (ip, sa)
                if key in seen:
                    continue
                seen.add(key)
                unique.append((ip, sa))
            return unique
        except Exception:
            return None

    def __repr__(self) -> str:
        return f"<_AddressListener services={sorted(self._services) if self._services else '*'} nameserver={self._nameserver!r}>"

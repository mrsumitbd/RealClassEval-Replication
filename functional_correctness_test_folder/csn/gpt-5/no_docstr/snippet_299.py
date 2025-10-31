class _AddressListener:

    def __init__(self, subscriber, services='', nameserver='localhost'):
        self.subscriber = subscriber
        # Normalize services into a set; empty set means accept all
        if services is None or services == '':
            self.services = set()
        elif isinstance(services, (list, tuple, set)):
            self.services = {str(s).strip().lower()
                             for s in services if str(s).strip()}
        elif isinstance(services, str):
            self.services = {s.strip().lower()
                             for s in services.split(',') if s.strip()}
        else:
            self.services = {str(services).strip().lower()} if str(
                services).strip() else set()

        # Store nameserver as provided (no external DNS lib used)
        self.nameserver = str(
            nameserver) if nameserver is not None else 'localhost'

    def handle_msg(self, msg):
        # Accept dict or JSON str/bytes
        data = None
        if isinstance(msg, dict):
            data = msg
        elif isinstance(msg, (str, bytes, bytearray)):
            try:
                import json
                text = msg.decode() if isinstance(msg, (bytes, bytearray)) else msg
                data = json.loads(text)
            except Exception:
                return False
        else:
            return False

        # Extract fields with fallbacks
        service = data.get('service') or data.get(
            'svc') or data.get('type') or ''
        service = str(service).strip()
        service_lc = service.lower()

        if self.services and service_lc not in self.services:
            return False

        address = data.get('address') or data.get(
            'addr') or data.get('host') or data.get('hostname') or ''
        port = data.get('port') or data.get('p') or None
        name = data.get('name') or data.get('id') or data.get('instance') or ''

        # Normalize port to int if possible
        try:
            port = int(port) if port is not None and port != '' else None
        except (ValueError, TypeError):
            port = None

        event = {
            'service': service if service else None,
            'address': str(address) if address is not None else None,
            'port': port,
            'name': str(name) if name is not None else None,
            'raw': data,
            'nameserver': self.nameserver,
        }

        # Dispatch to subscriber
        handled = False
        try:
            if hasattr(self.subscriber, 'on_address') and callable(getattr(self.subscriber, 'on_address')):
                self.subscriber.on_address(event)
                handled = True
            elif callable(self.subscriber):
                self.subscriber(event)
                handled = True
            elif hasattr(self.subscriber, 'put') and callable(getattr(self.subscriber, 'put')):
                self.subscriber.put(event)
                handled = True
        except Exception:
            return False

        return handled

class _AddressListener:

    def __init__(self, subscriber, services='', nameserver='localhost'):
        '''Initialize address listener.'''
        self.subscriber = subscriber
        self.nameserver = nameserver
        if services is None:
            services = ''
        if isinstance(services, str):
            tokens = [s.strip() for s in services.replace(
                ';', ',').split(',') if s.strip()]
        else:
            try:
                tokens = [str(s).strip() for s in services if str(s).strip()]
            except TypeError:
                tokens = []
        self._services = set(s.lower() for s in tokens)

    def _normalize_msg(self, msg):
        import json
        # Convert bytes to str
        if isinstance(msg, (bytes, bytearray)):
            try:
                msg = msg.decode('utf-8', errors='ignore')
            except Exception:
                msg = str(msg)

        # If it's a string, try JSON then key=value parsing
        if isinstance(msg, str):
            s = msg.strip()
            if not s:
                return {}
            # Try JSON
            try:
                obj = json.loads(s)
                if isinstance(obj, dict):
                    msg = obj
                elif isinstance(obj, list) and obj and isinstance(obj[0], dict):
                    msg = obj[0]
                else:
                    # Fallthrough to manual parsing
                    raise ValueError
            except Exception:
                # Manual parsing: accept "key=value" tokens separated by commas or whitespace
                data = {}
                # If it's exactly two space-separated tokens without equals, treat as service and address
                parts_ws = s.split()
                if len(parts_ws) == 2 and '=' not in s:
                    data['service'] = parts_ws[0]
                    data['address'] = parts_ws[1]
                    msg = data
                else:
                    # Split by commas first, then by whitespace for remaining
                    candidates = []
                    for chunk in s.split(','):
                        chunk = chunk.strip()
                        if not chunk:
                            continue
                        candidates.extend(x for x in chunk.split() if x)
                    for token in candidates:
                        if '=' in token:
                            k, v = token.split('=', 1)
                            data[k.strip()] = v.strip()
                    msg = data

        # If it's not a dict now, try to coerce to dict
        if not isinstance(msg, dict):
            try:
                # Best effort: wrap as address only
                return {'address': str(msg)}
            except Exception:
                return {}

        # Normalize keys to lowercase and strip values
        norm = {}
        for k, v in msg.items():
            key = str(k).lower().strip()
            if isinstance(v, (str, bytes, bytearray)):
                if isinstance(v, (bytes, bytearray)):
                    try:
                        v = v.decode('utf-8', errors='ignore')
                    except Exception:
                        v = str(v)
                v = v.strip()
            norm[key] = v

        # Canonical aliases
        if 'svc' in norm and 'service' not in norm:
            norm['service'] = norm.pop('svc')
        if 'addr' in norm and 'address' not in norm:
            norm['address'] = norm.pop('addr')
        if 'ns' in norm and 'nameserver' not in norm:
            norm['nameserver'] = norm.pop('ns')

        return norm

    def _passes_filters(self, data):
        # Services filter
        service = str(data.get('service', '')).lower(
        ) if data.get('service') is not None else ''
        if self._services and service not in self._services:
            return False
        # Nameserver filter (if provided in message)
        msg_ns = data.get('nameserver')
        if msg_ns is not None and str(msg_ns) != str(self.nameserver):
            return False
        return True

    def _dispatch(self, payload):
        target = self.subscriber
        # Prefer explicit callback
        cb = getattr(target, 'on_address', None)
        if callable(cb):
            cb(payload)
            return True
        # Common queue/list interfaces
        for method_name in ('put', 'append', 'send', 'write'):
            m = getattr(target, method_name, None)
            if callable(m):
                m(payload)
                return True
        # Callable subscriber
        if callable(target):
            target(payload)
            return True
        # Attribute to store last message as fallback
        try:
            setattr(target, 'last_address_message', payload)
            return True
        except Exception:
            return False

    def handle_msg(self, msg):
        '''Handle the message *msg*.'''
        data = self._normalize_msg(msg)
        if not data:
            return None
        if not self._passes_filters(data):
            return None
        self._dispatch(data)
        return data

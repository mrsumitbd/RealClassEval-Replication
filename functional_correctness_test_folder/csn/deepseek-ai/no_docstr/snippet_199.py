
class UriParam:

    def __init__(self, uri):
        self.uri = uri
        self.params = {}
        if '?' in uri:
            parts = uri.split('?')
            if len(parts) > 1:
                query = parts[1]
                pairs = query.split('&')
                for pair in pairs:
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        self.params[key] = value

    def __repr__(self):
        param_str = ', '.join(f"{k}={v}" for k, v in self.params.items())
        return f"UriParam(uri='{self.uri}', params={{{param_str}}})"

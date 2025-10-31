class CodePageManager:

    def __init__(self, data):
        self.data = {}
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, (list, tuple, set)):
                    for alias in v:
                        if isinstance(alias, str):
                            self.data[alias.strip().lower()] = k
                else:
                    if isinstance(k, str) and isinstance(v, str):
                        self.data[k.strip().lower()] = v.strip().lower()

    @staticmethod
    def get_encoding_name(encoding):
        import codecs

        if encoding is None:
            return None

        if isinstance(encoding, bytes):
            try:
                encoding = encoding.decode('ascii', errors='strict')
            except Exception:
                return None

        if isinstance(encoding, int):
            name = f'cp{encoding}'
        elif isinstance(encoding, str):
            name = encoding.strip().lower()
            name = name.replace('_', '-')
            if name.startswith('windows-') and name[8:].isdigit():
                name = 'cp' + name[8:]
            elif name.startswith('cp-') and name[3:].isdigit():
                name = 'cp' + name[3:]
        else:
            return None

        try:
            return codecs.lookup(name).name
        except Exception:
            # Try some common fallbacks
            if isinstance(name, str):
                # remove dashes and try
                compact = name.replace('-', '')
                try:
                    return codecs.lookup(compact).name
                except Exception:
                    pass
                # try adding cp for digits
                if name.isdigit():
                    try:
                        return codecs.lookup('cp' + name).name
                    except Exception:
                        pass
            return None

    def get_encoding_name(encoding):
        import codecs

        if encoding is None:
            return None

        if isinstance(encoding, bytes):
            try:
                encoding = encoding.decode('ascii', errors='strict')
            except Exception:
                return None

        if isinstance(encoding, int):
            name = f'cp{encoding}'
        elif isinstance(encoding, str):
            name = encoding.strip().lower()
            name = name.replace('_', '-')
            if name.startswith('windows-') and name[8:].isdigit():
                name = 'cp' + name[8:]
            elif name.startswith('cp-') and name[3:].isdigit():
                name = 'cp' + name[3:]
        else:
            return None

        try:
            return codecs.lookup(name).name
        except Exception:
            if isinstance(name, str):
                compact = name.replace('-', '')
                try:
                    return codecs.lookup(compact).name
                except Exception:
                    pass
                if name.isdigit():
                    try:
                        return codecs.lookup('cp' + name).name
                    except Exception:
                        pass
            return None

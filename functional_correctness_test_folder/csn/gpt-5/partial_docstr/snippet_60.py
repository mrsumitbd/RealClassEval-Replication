class CodePageManager:
    '''Holds information about all the code pages.
    Information as defined in escpos-printer-db.
        '''

    def __init__(self, data):
        self._raw = data
        self._encodings = {}

        if isinstance(data, dict):
            items = data.items()
        else:
            try:
                items = enumerate(data)
            except TypeError:
                items = ()

        for key, info in items:
            if isinstance(info, dict):
                # Primary identifier from dict key if it's a str, else from info
                identifiers = []
                if isinstance(key, str):
                    identifiers.append(key)
                enc = info.get("encoding")
                if isinstance(enc, str):
                    identifiers.append(enc)
                # also common aliases inside info
                for alias_key in ("aliases", "alias", "names", "name"):
                    aliases = info.get(alias_key)
                    if isinstance(aliases, str):
                        identifiers.append(aliases)
                    elif isinstance(aliases, (list, tuple, set)):
                        identifiers.extend(
                            [a for a in aliases if isinstance(a, str)])

                # Build normalized map
                for ident in identifiers:
                    norm = self._normalize_encoding(ident)
                    if norm and norm not in self._encodings:
                        self._encodings[norm] = info
                        # also store canonical python codec name if present
                        if isinstance(enc, str):
                            pyname = self._normalize_encoding(enc)
                            if pyname and pyname not in self._encodings:
                                self._encodings[pyname] = info
            else:
                # if info is not dict, try to treat as string encoding name
                if isinstance(info, str):
                    norm = self._normalize_encoding(info)
                    if norm and norm not in self._encodings:
                        self._encodings[norm] = {"encoding": info}

                if isinstance(key, str):
                    normk = self._normalize_encoding(key)
                    if normk and normk not in self._encodings:
                        self._encodings[normk] = {"encoding": key}

    @staticmethod
    def _normalize_encoding(encoding):
        if encoding is None:
            return None
        if not isinstance(encoding, str):
            encoding = str(encoding)
        s = encoding.strip().lower()

        # Remove common separators
        for ch in [' ', '-', '_', '.', '/']:
            s = s.replace(ch, '')

        # Normalize common vendor prefixes
        if s.startswith('windows'):
            s = 'cp' + s[len('windows'):]
        if s.startswith('ibm'):
            s = 'cp' + s[len('ibm'):]
        if s.startswith('ms'):
            s = 'cp' + s[len('ms'):]
        if s.startswith('cp-'):
            s = 'cp' + s[3:]

        # Trim 'cs' registry prefix
        if s.startswith('cs') and s not in ('cskoi8r',):
            s = s[2:]

        # Common special cases
        if s in ('utf8', 'utf'):
            s = 'utf8'
        elif s in ('utf16', 'utf16le', 'utf16be'):
            s = s
        elif s in ('utf32', 'utf32le', 'utf32be'):
            s = s
        elif s in ('latin1', 'latin'):
            s = 'iso88591'
        elif s.startswith('iso8859'):
            s = s

        return s or None

    def get_encoding_name(*args):
        '''Return the encoding data.'''
        # Support both instance and class-style calls.
        if len(args) == 2:
            self, encoding = args
            norm = CodePageManager._normalize_encoding(encoding)
            if norm is None:
                return None
            # Direct hit
            info = getattr(self, "_encodings", {}).get(norm)
            if info is not None:
                return info
            # Try alternative fallbacks
            # utf-8 variants
            if norm in ('utf8', 'utf_8'):
                return getattr(self, "_encodings", {}).get('utf8')
            # cp vs windows prefixes
            if norm.startswith('cp'):
                alt = 'windows' + norm[2:]
                info = getattr(self, "_encodings", {}).get(
                    CodePageManager._normalize_encoding(alt))
                if info is not None:
                    return info
            if norm.startswith('windows'):
                alt = 'cp' + norm[len('windows'):]
                info = getattr(self, "_encodings", {}).get(
                    CodePageManager._normalize_encoding(alt))
                if info is not None:
                    return info
            return None
        elif len(args) == 1:
            # Called as CodePageManager.get_encoding_name(encoding): return normalized name
            encoding = args[0]
            return CodePageManager._normalize_encoding(encoding)
        else:
            raise TypeError("get_encoding_name expected 1 or 2 arguments")

class TnsFilter:

    def __init__(self, *tns):
        self._tokens = set()
        if tns:
            self.add(*tns)

    def _flatten_tokens(self, *tns):
        for t in tns:
            if t is None:
                continue
            if isinstance(t, (list, tuple, set)):
                for x in self._flatten_tokens(*t):
                    yield x
            else:
                s = str(t)
                for part in s.split():
                    if part:
                        yield part

    def add(self, *tns):
        for token in self._flatten_tokens(*tns):
            self._tokens.add(token)
        return self

    def match(self, root, ns):
        # Normalize namespace to empty string for no-namespace
        ns_norm = '' if (ns is None or ns == '') else ns

        # If no tokens were provided, default to match any
        if not self._tokens:
            return True

        # Obtain targetNamespace from root element if available
        root_tns = ''
        if root is not None:
            # Try dictionary-like access (e.g., xml.etree.ElementTree.Element)
            try:
                root_tns = root.get('targetNamespace') or ''
            except Exception:
                # Fallback: attribute access or mapping
                try:
                    root_tns = getattr(root, 'targetNamespace', '') or ''
                except Exception:
                    root_tns = ''

        for token in self._tokens:
            if token == '##any':
                return True
            if token == '##local':
                if ns_norm == '':
                    return True
            elif token == '##targetNamespace':
                if ns_norm == root_tns:
                    return True
            elif token == '##other':
                # Any namespace other than the target namespace
                if ns_norm != root_tns:
                    return True
            else:
                if ns_norm == token:
                    return True

        return False

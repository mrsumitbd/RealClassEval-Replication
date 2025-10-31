class CkClass:
    '''
    Base class for CK_* classes
    '''

    def _get_module(self):
        import sys
        return sys.modules.get(self.__class__.__module__)

    def _iter_flag_defs(self):
        # Priority: explicit mappings on the instance/class if provided
        # 1) FLAG_MAP: dict {bit:int -> name:str}
        flag_map = getattr(self, 'FLAG_MAP', None) or getattr(
            self.__class__, 'FLAG_MAP', None)
        if isinstance(flag_map, dict):
            for bit, name in flag_map.items():
                if isinstance(bit, int) and isinstance(name, str):
                    yield (bit, name)
            return

        # 2) FLAGS: iterable of (bit, name) or name->bit
        flags = getattr(self, 'FLAGS', None) or getattr(
            self.__class__, 'FLAGS', None)
        if flags is not None:
            try:
                for item in flags:
                    if isinstance(item, tuple) and len(item) == 2:
                        a, b = item
                        if isinstance(a, int) and isinstance(b, str):
                            yield (a, b)
                        elif isinstance(a, str) and isinstance(b, int):
                            yield (b, a)
                    elif isinstance(item, int):
                        # If only bit is given, synthesize a name
                        yield (item, f'CKF_0x{item:X}')
                    elif isinstance(item, str):
                        # Try resolve name from class/module
                        value = getattr(self, item, None)
                        if not isinstance(value, int):
                            value = getattr(self.__class__, item, None)
                        if not isinstance(value, int):
                            mod = self._get_module()
                            value = getattr(mod, item, None) if mod else None
                        if isinstance(value, int):
                            yield (value, item)
            except TypeError:
                pass
            return

        # 3) Fallback: scan class and module for CKF_* integer constants
        seen = {}
        # from class
        for name in dir(self.__class__):
            if not name.startswith('CKF_'):
                continue
            val = getattr(self.__class__, name, None)
            if isinstance(val, int):
                seen.setdefault(val, name)
        # from module
        mod = self._get_module()
        if mod:
            for name in dir(mod):
                if not name.startswith('CKF_'):
                    continue
                val = getattr(mod, name, None)
                if isinstance(val, int) and val not in seen:
                    seen[val] = name
        for bit, name in seen.items():
            yield (bit, name)

    def flags2text(self):
        '''
        parse the `self.flags` field and create a list of `CKF_*` strings
        corresponding to bits set in flags
        :return: a list of strings
        :rtype: list
        '''
        f = getattr(self, 'flags', 0) or 0
        try:
            f_int = int(f)
        except Exception:
            f_int = 0
        pairs = list(self._iter_flag_defs())
        # Sort by bit value for deterministic ordering
        pairs.sort(key=lambda x: (x[0], x[1]))
        result = []
        used_bits = 0
        for bit, name in pairs:
            if bit and (f_int & bit) == bit:
                result.append(name)
                used_bits |= bit
        # If there are remaining bits without names, include generic CKF_0x...
        remaining = f_int & ~used_bits
        if remaining:
            # Decompose remaining into individual set bits
            x = remaining
            while x:
                b = x & -x
                result.append(f'CKF_0x{b:X}')
                x ^= b
        return result

    def state2text(self):
        '''
        Dummy method. Will be overwriden if necessary
        '''
        state = getattr(self, 'state', None)
        if state is None:
            return None
        # Priority: explicit mappings
        state_map = getattr(self, 'STATE_MAP', None) or getattr(
            self.__class__, 'STATE_MAP', None)
        if isinstance(state_map, dict):
            return state_map.get(state) or state_map.get(int(state), None)

        # Try STATES iterable similar to FLAGS
        states = getattr(self, 'STATES', None) or getattr(
            self.__class__, 'STATES', None)
        if states is not None:
            try:
                for item in states:
                    if isinstance(item, tuple) and len(item) == 2:
                        a, b = item
                        if isinstance(a, int) and a == state and isinstance(b, str):
                            return b
                        if isinstance(b, int) and b == state and isinstance(a, str):
                            return a
                    elif isinstance(item, str):
                        val = getattr(self, item, None)
                        if not isinstance(val, int):
                            val = getattr(self.__class__, item, None)
                        if not isinstance(val, int):
                            mod = self._get_module()
                            val = getattr(mod, item, None) if mod else None
                        if isinstance(val, int) and val == state:
                            return item
            except TypeError:
                pass

        # Fallback: search module/class for CKS_* exact match
        mod = self._get_module()
        candidates = []
        for name in dir(self.__class__):
            if name.startswith('CKS_'):
                val = getattr(self.__class__, name, None)
                if isinstance(val, int) and val == state:
                    candidates.append(name)
        if mod:
            for name in dir(mod):
                if name.startswith('CKS_'):
                    val = getattr(mod, name, None)
                    if isinstance(val, int) and val == state:
                        candidates.append(name)
        if candidates:
            # Deterministic: smallest lexicographically
            candidates.sort()
            return candidates[0]

        # Default textual representation
        try:
            return f'0x{int(state):X}'
        except Exception:
            return str(state)

    def to_dict(self):
        '''
        convert the fields of the object into a dictionnary
        '''
        def convert(val):
            if isinstance(val, CkClass):
                return val.to_dict()
            if hasattr(val, 'to_dict') and callable(val.to_dict):
                try:
                    return val.to_dict()
                except Exception:
                    pass
            if isinstance(val, (list, tuple)):
                return type(val)(convert(v) for v in val)
            if isinstance(val, memoryview):
                return bytes(val)
            return val

        data = {}
        for k, v in vars(self).items():
            if k.startswith('_') or callable(v):
                continue
            data[k] = convert(v)

        # Add textual helpers if applicable
        if 'flags' in data:
            try:
                data['flags_text'] = self.flags2text()
            except Exception:
                pass
        if 'state' in data:
            try:
                data['state_text'] = self.state2text()
            except Exception:
                pass

        return data

    def __str__(self):
        '''
        text representation of the object
        '''
        try:
            d = self.to_dict()
        except Exception:
            d = {k: v for k, v in vars(self).items(
            ) if not k.startswith('_') and not callable(v)}
        items = ', '.join(f'{k}={repr(v)}' for k, v in sorted(d.items()))
        return f'{self.__class__.__name__}({items})'

from typing import Union, overload

class _Quoter:

    def __init__(self, *, safe: str='', protected: str='', qs: bool=False, requote: bool=True) -> None:
        self._safe = safe
        self._protected = protected
        self._qs = qs
        self._requote = requote

    @overload
    def __call__(self, val: str) -> str:
        ...

    @overload
    def __call__(self, val: None) -> None:
        ...

    def __call__(self, val: Union[str, None]) -> Union[str, None]:
        if val is None:
            return None
        if not isinstance(val, str):
            raise TypeError('Argument should be str')
        if not val:
            return ''
        bval = val.encode('utf8', errors='ignore')
        ret = bytearray()
        pct = bytearray()
        safe = self._safe
        safe += ALLOWED
        if not self._qs:
            safe += '+&=;'
        safe += self._protected
        bsafe = safe.encode('ascii')
        idx = 0
        while idx < len(bval):
            ch = bval[idx]
            idx += 1
            if pct:
                if ch in BASCII_LOWERCASE:
                    ch = ch - 32
                pct.append(ch)
                if len(pct) == 3:
                    buf = pct[1:]
                    if not _IS_HEX.match(buf):
                        ret.extend(b'%25')
                        pct.clear()
                        idx -= 2
                        continue
                    try:
                        unquoted = chr(int(pct[1:].decode('ascii'), base=16))
                    except ValueError:
                        ret.extend(b'%25')
                        pct.clear()
                        idx -= 2
                        continue
                    if unquoted in self._protected:
                        ret.extend(pct)
                    elif unquoted in safe:
                        ret.append(ord(unquoted))
                    else:
                        ret.extend(pct)
                    pct.clear()
                elif len(pct) == 2 and idx == len(bval):
                    ret.extend(b'%25')
                    pct.clear()
                    idx -= 1
                continue
            elif ch == ord('%') and self._requote:
                pct.clear()
                pct.append(ch)
                if idx == len(bval):
                    ret.extend(b'%25')
                continue
            if self._qs and ch == ord(' '):
                ret.append(ord('+'))
                continue
            if ch in bsafe:
                ret.append(ch)
                continue
            ret.extend(f'%{ch:02X}'.encode('ascii'))
        ret2 = ret.decode('ascii')
        if ret2 == val:
            return val
        return ret2
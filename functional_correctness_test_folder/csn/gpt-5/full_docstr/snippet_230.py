class RawPacket:
    '''RawPacket
    Wraps a packet such that:
        packet.raw.fieldname
    returns the value of fieldname as a raw value with no enumeration
    substitutions or DN to EU conversions applied.
    '''

    def __init__(self, packet):
        '''Creates a new RawPacket based on the given Packet.'''
        self._packet = packet

    def __getattr__(self, fieldname):
        '''Returns the value of the given packet fieldname as a raw
        value with no DN to EU conversion applied.
        '''
        p = self._packet

        def try_call(fn):
            try:
                return True, fn()
            except Exception:
                return False, None

        attempts = [
            # Common explicit API styles
            lambda: p.get_raw_value(fieldname),
            lambda: p.get_value(fieldname, raw=True),
            lambda: p.get(fieldname, raw=True),
            # Field accessor objects
            lambda: getattr(p, 'get_field')(fieldname).raw,
            lambda: getattr(p, 'get_field')(fieldname).raw_value,
            # Indexing by field name
            lambda: p[fieldname].raw,
            lambda: p[fieldname].raw_value,
            # Field maps
            lambda: p.fields[fieldname].raw,
            lambda: p.fields[fieldname].raw_value,
            # Internal maps
            lambda: p._raw[fieldname],
            lambda: p._raw_values[fieldname],
            lambda: p._values[fieldname]['raw'],
            # Alternate field containers
            lambda: getattr(getattr(p, 'fields_map'), fieldname).raw,
            # Attribute-based field objects
            lambda: getattr(getattr(p, fieldname), 'raw'),
            lambda: getattr(getattr(p, fieldname), 'raw_value'),
            lambda: getattr(getattr(p, fieldname), 'dn'),
        ]

        for fn in attempts:
            ok, val = try_call(fn)
            if ok:
                return val

        # Fallback: delegate to the packet's attribute if it exists
        try:
            return getattr(p, fieldname)
        except AttributeError:
            raise AttributeError(
                f"No raw value found for field '{fieldname}'") from None

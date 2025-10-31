class RawPacket:

    def __init__(self, packet):
        self._packet = packet

    def __getattr__(self, fieldname):
        '''Returns the value of the given packet fieldname as a raw
        value with no DN to EU conversion applied.
        '''
        pkt = self._packet

        # 1) Dedicated raw accessors/mappings
        if hasattr(pkt, 'get_raw') and callable(getattr(pkt, 'get_raw')):
            return pkt.get_raw(fieldname)
        if hasattr(pkt, 'getRaw') and callable(getattr(pkt, 'getRaw')):
            return pkt.getRaw(fieldname)
        if hasattr(pkt, 'raw'):
            raw_attr = getattr(pkt, 'raw')
            try:
                return raw_attr[fieldname]
            except Exception:
                pass

        # 2) Common field containers
        for container_name in ('fields', 'field_map', 'field', 'attributes'):
            if hasattr(pkt, container_name):
                container = getattr(pkt, container_name)
                # Mapping-like container
                try:
                    fld = container[fieldname]
                    # Try common raw attributes on the field
                    for raw_name in ('raw', 'raw_value', 'dn', 'value_dn'):
                        if hasattr(fld, raw_name):
                            return getattr(fld, raw_name)
                    return fld
                except Exception:
                    pass

        # 3) Attribute on packet that may itself expose a raw value
        if hasattr(pkt, fieldname):
            fld = getattr(pkt, fieldname)
            for raw_name in ('raw', 'raw_value', 'dn', 'value_dn'):
                if hasattr(fld, raw_name):
                    return getattr(fld, raw_name)
            return fld

        # 4) Item access on packet
        if hasattr(pkt, '__getitem__'):
            try:
                fld = pkt[fieldname]
                for raw_name in ('raw', 'raw_value', 'dn', 'value_dn'):
                    if hasattr(fld, raw_name):
                        return getattr(fld, raw_name)
                return fld
            except Exception:
                pass

        raise AttributeError(
            f"{type(self).__name__} has no field '{fieldname}' and underlying packet does not expose a raw value for it")

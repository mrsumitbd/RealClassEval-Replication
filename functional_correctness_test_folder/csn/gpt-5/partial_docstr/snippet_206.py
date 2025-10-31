class StreamCodeDebug:

    _TYPE_CODES = {
        0x70: "TC_NULL",
        0x71: "TC_REFERENCE",
        0x72: "TC_CLASSDESC",
        0x73: "TC_OBJECT",
        0x74: "TC_STRING",
        0x75: "TC_ARRAY",
        0x76: "TC_CLASS",
        0x77: "TC_BLOCKDATA",
        0x78: "TC_ENDBLOCKDATA",
        0x79: "TC_RESET",
        0x7A: "TC_BLOCKDATALONG",
        0x7B: "TC_EXCEPTION",
        0x7C: "TC_LONGSTRING",
        0x7D: "TC_PROXYCLASSDESC",
        0x7E: "TC_ENUM",
    }

    _FLAG_BITS = {
        0x01: "SC_WRITE_METHOD",
        0x02: "SC_SERIALIZABLE",
        0x04: "SC_EXTERNALIZABLE",
        0x08: "SC_BLOCK_DATA",
        0x10: "SC_ENUM",
    }

    @staticmethod
    def op_id(op_id):
        try:
            if op_id in StreamCodeDebug._TYPE_CODES:
                return StreamCodeDebug._TYPE_CODES[op_id]
            return f"UNKNOWN_OP(0x{op_id:02X})"
        except Exception:
            return "UNKNOWN_OP"

    @staticmethod
    def type_code(type_id):
        '''
        Returns the name of the given Type Code
        :param type_id: Type code
        :return: Name of the type code
        '''
        try:
            return StreamCodeDebug._TYPE_CODES.get(type_id, f"UNKNOWN_TC(0x{type_id:02X})")
        except Exception:
            return "UNKNOWN_TC"

    @staticmethod
    def flags(flags):
        '''
        Returns the names of the class description flags found in the given
        integer
        :param flags: A class description flag entry
        :return: The flags names as a single string
        '''
        try:
            names = []
            remaining = flags
            for bit, name in sorted(StreamCodeDebug._FLAG_BITS.items()):
                if flags & bit:
                    names.append(name)
                    remaining &= ~bit
            if remaining:
                names.append(f"UNKNOWN_FLAGS(0x{remaining:02X})")
            return " | ".join(names) if names else ""
        except Exception:
            return ""


class StreamCodeDebug:

    @staticmethod
    def op_id(op_id):
        op_map = {
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
            0x7E: "TC_ENUM"
        }
        return op_map.get(op_id, f"UNKNOWN_OP_ID({hex(op_id)})")

    @staticmethod
    def type_code(type_id):
        '''
        Returns the name of the given Type Code
        :param type_id: Type code
        :return: Name of the type code
        '''
        type_map = {
            b'B': "byte",
            b'C': "char",
            b'D': "double",
            b'F': "float",
            b'I': "int",
            b'J': "long",
            b'S': "short",
            b'Z': "boolean",
            b'L': "object",
            b'[': "array"
        }
        # Accept both bytes and str
        if isinstance(type_id, str):
            type_id = type_id.encode()
        return type_map.get(type_id, f"UNKNOWN_TYPE_CODE({type_id.decode(errors='replace')})")

    @staticmethod
    def flags(flags):
        '''
        Returns the names of the class description flags found in the given
        integer
        :param flags: A class description flag entry
        :return: The flags names as a single string
        '''
        flag_map = {
            0x01: "SC_WRITE_METHOD",
            0x02: "SC_BLOCK_DATA",
            0x04: "SC_SERIALIZABLE",
            0x08: "SC_EXTERNALIZABLE",
            0x10: "SC_ENUM"
        }
        names = []
        for bit, name in flag_map.items():
            if flags & bit:
                names.append(name)
        if not names:
            return "NONE"
        return "|".join(names)

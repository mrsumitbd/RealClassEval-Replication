class StreamCodeDebug:
    '''
    Codes utility methods
    '''

    _OPCODES = {
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

    _TYPECODES = {
        'B': "byte",
        'C': "char",
        'D': "double",
        'F': "float",
        'I': "int",
        'J': "long",
        'L': "object",
        'S': "short",
        'Z': "boolean",
        '[': "array",
    }

    _FLAGS = [
        (0x01, "SC_WRITE_METHOD"),
        (0x02, "SC_SERIALIZABLE"),
        (0x04, "SC_EXTERNALIZABLE"),
        (0x08, "SC_BLOCK_DATA"),
        (0x10, "SC_ENUM"),
    ]

    @staticmethod
    def op_id(op_id):
        '''
        Returns the name of the given OP Code
        :param op_id: OP Code
        :return: Name of the OP Code
        '''
        # Normalize integers possibly given as bytes
        if isinstance(op_id, (bytes, bytearray)) and len(op_id) == 1:
            op_id = op_id[0]
        try:
            op_int = int(op_id)
        except Exception:
            return "UNKNOWN"
        return StreamCodeDebug._OPCODES.get(op_int & 0xFF, "UNKNOWN")

    @staticmethod
    def type_code(type_id):
        '''
        Returns the name of the given Type Code
        :param type_id: Type code
        :return: Name of the type code
        '''
        if isinstance(type_id, (bytes, bytearray)):
            if len(type_id) == 0:
                return "UNKNOWN"
            type_id = chr(type_id[0])
        elif isinstance(type_id, int):
            if 0 <= type_id <= 0x10FFFF:
                type_id = chr(type_id)
            else:
                return "UNKNOWN"
        elif not isinstance(type_id, str) or len(type_id) == 0:
            return "UNKNOWN"
        return StreamCodeDebug._TYPECODES.get(type_id[0], "UNKNOWN")

    @staticmethod
    def flags(flags):
        '''
        Returns the names of the class description flags found in the given
        integer
        :param flags: A class description flag entry
        :return: The flags names as a single string
        '''
        try:
            val = int(flags)
        except Exception:
            return "UNKNOWN"
        names = [name for bit, name in StreamCodeDebug._FLAGS if val & bit]
        return " | ".join(names) if names else "0"

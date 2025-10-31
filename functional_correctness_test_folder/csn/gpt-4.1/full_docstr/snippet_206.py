
class StreamCodeDebug:
    '''
    Codes utility methods
    '''
    # Example OP Codes mapping (can be extended)
    _OP_CODES = {
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

    # Example Type Codes mapping (can be extended)
    _TYPE_CODES = {
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

    # Example Flags mapping (can be extended)
    _FLAGS = {
        0x01: "SC_WRITE_METHOD",
        0x02: "SC_BLOCK_DATA",
        0x04: "SC_SERIALIZABLE",
        0x08: "SC_EXTERNALIZABLE",
        0x10: "SC_ENUM",
    }

    @staticmethod
    def op_id(op_id):
        '''
        Returns the name of the given OP Code
        :param op_id: OP Code
        :return: Name of the OP Code
        '''
        return StreamCodeDebug._OP_CODES.get(op_id, f"UNKNOWN_OP_CODE({op_id})")

    @staticmethod
    def type_code(type_id):
        '''
        Returns the name of the given Type Code
        :param type_id: Type code
        :return: Name of the type code
        '''
        return StreamCodeDebug._TYPE_CODES.get(type_id, f"UNKNOWN_TYPE_CODE({type_id})")

    @staticmethod
    def flags(flags):
        '''
        Returns the names of the class description flags found in the given
        integer
        :param flags: A class description flag entry
        :return: The flags names as a single string
        '''
        names = []
        for bit, name in StreamCodeDebug._FLAGS.items():
            if flags & bit:
                names.append(name)
        if not names:
            return "NO_FLAGS"
        return "|".join(names)

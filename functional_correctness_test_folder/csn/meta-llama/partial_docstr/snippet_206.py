
class StreamCodeDebug:
    """
    A utility class for debugging Java Object Serialization Stream Codes.
    """

    # Mapping of operation IDs to their corresponding names
    OP_ID_MAPPING = {
        0x70: 'TC_NULL',
        0x71: 'TC_REFERENCE',
        0x72: 'TC_CLASS',
        0x73: 'TC_OBJECT',
        0x74: 'TC_STRING',
        0x75: 'TC_ARRAY',
        0x76: 'TC_CLASSDESC',
        0x77: 'TC_PROXYCLASSDESC',
        0x78: 'TC_ENUM',
        0x79: 'TC_BLOCKDATA',
        0x7A: 'TC_BLOCKDATALONG',
        0x7B: 'TC_RESET',
        0x7C: 'TC_BLOCKDATAEMPTY',
        0x7D: 'TC_EXCEPTION'
    }

    # Mapping of type codes to their corresponding names
    TYPE_CODE_MAPPING = {
        'B': 'byte',
        'C': 'char',
        'D': 'double',
        'F': 'float',
        'I': 'int',
        'J': 'long',
        'L': 'object',
        'S': 'short',
        'Z': 'boolean',
        '[': 'array'
    }

    # Mapping of class description flags to their corresponding names
    CLASS_DESCRIPTION_FLAGS_MAPPING = {
        0x01: 'SC_WRITE_METHOD',
        0x02: 'SC_BLOCK_DATA',
        0x04: 'SC_SERIALIZABLE',
        0x08: 'SC_EXTERNALIZABLE',
        0x10: 'SC_ENUM'
    }

    @staticmethod
    def op_id(op_id):
        return StreamCodeDebug.OP_ID_MAPPING.get(op_id, f"Unknown OP ID: {op_id:#04x}")

    @staticmethod
    def type_code(type_id):
        return StreamCodeDebug.TYPE_CODE_MAPPING.get(type_id, f"Unknown Type Code: {type_id}")

    @staticmethod
    def flags(flags):
        flag_names = [
            name for flag, name in StreamCodeDebug.CLASS_DESCRIPTION_FLAGS_MAPPING.items() if flags & flag]
        return ' | '.join(flag_names) if flag_names else 'No flags'

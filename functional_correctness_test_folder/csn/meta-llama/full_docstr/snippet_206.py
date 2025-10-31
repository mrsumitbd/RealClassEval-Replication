
class StreamCodeDebug:
    '''
    Codes utility methods
    '''
    OP_CODES = {
        0x70: 'NEW',
        0x71: 'REF',
        0x72: 'NULL',
        0x73: 'CLASS',
        0x74: 'OBJECT',
        0x75: 'ARRAY',
        0x76: 'SEND',
        0x77: 'EXCEPTION',
        0x78: 'TC_RESET',
        0x79: 'CAST',
        0x7A: 'CAST_FAIL',
        0x7B: 'EXTENDED',
        0x7C: 'GRT',
        0x7D: 'GRT_LIST',
        0x7E: 'NOOP',
        0xC0: 'CLASSDESC',
        0xC1: 'NULLCLASSDESC',
        0xC2: 'PROXYCLASSDESC',
        0xC3: 'ENUM',
        0xC4: 'BLOCKDATA',
        0xC5: 'BLOCKDATALONG',
        0xC6: 'RESET',
        0xC7: 'BLOCKDATA',
        0xC8: 'ENDBLOCKDATA'
    }

    TYPE_CODES = {
        0x70: 'TC_NULL',
        0x71: 'TC_REFERENCE',
        0x72: 'TC_CLASS',
        0x73: 'TC_OBJECT',
        0x74: 'TC_ARRAY',
        0x75: 'TC_STRING',
        0x76: 'TC_ENUM',
        0x77: 'TC_CLASSDESC',
        0x78: 'TC_PROXYCLASSDESC',
        0x79: 'TC_ENUM',
        0x7A: 'TC_BLOCKDATA',
        0x7B: 'TC_ENDBLOCKDATA',
        0x7C: 'TC_RESET'
    }

    CLASS_DESCRIPTION_FLAGS = {
        0x01: 'SC_WRITE_METHOD',
        0x02: 'SC_BLOCK_DATA',
        0x04: 'SC_SERIALIZABLE',
        0x08: 'SC_EXTERNALIZABLE',
        0x10: 'SC_ENUM'
    }

    @staticmethod
    def op_id(op_id):
        '''
        Returns the name of the given OP Code
        :param op_id: OP Code
        :return: Name of the OP Code
        '''
        return StreamCodeDebug.OP_CODES.get(op_id, f'UNKNOWN({op_id:#04x})')

    @staticmethod
    def type_code(type_id):
        '''
        Returns the name of the given Type Code
        :param type_id: Type code
        :return: Name of the type code
        '''
        return StreamCodeDebug.TYPE_CODES.get(type_id, f'UNKNOWN({type_id:#04x})')

    @staticmethod
    def flags(flags):
        '''
        Returns the names of the class description flags found in the given
        integer
        :param flags: A class description flag entry
        :return: The flags names as a single string
        '''
        flag_names = [
            name for mask, name in StreamCodeDebug.CLASS_DESCRIPTION_FLAGS.items() if flags & mask]
        return ' | '.join(flag_names) if flag_names else '0'

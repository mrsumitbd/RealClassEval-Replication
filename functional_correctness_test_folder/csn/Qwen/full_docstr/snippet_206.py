
class StreamCodeDebug:
    '''
    Codes utility methods
    '''
    OP_CODES = {
        0: 'NOP',
        1: 'LOAD',
        2: 'STORE',
        3: 'ADD',
        4: 'SUB',
        5: 'MUL',
        6: 'DIV',
        7: 'JMP',
        8: 'CALL',
        9: 'RET'
    }

    TYPE_CODES = {
        0: 'VOID',
        1: 'INT',
        2: 'FLOAT',
        3: 'STRING',
        4: 'BOOL',
        5: 'OBJECT',
        6: 'ARRAY'
    }

    FLAG_NAMES = {
        0x0001: 'PUBLIC',
        0x0002: 'PRIVATE',
        0x0004: 'PROTECTED',
        0x0008: 'STATIC',
        0x0010: 'FINAL',
        0x0020: 'SYNCHRONIZED',
        0x0040: 'VOLATILE',
        0x0080: 'TRANSIENT',
        0x0100: 'NATIVE',
        0x0200: 'INTERFACE',
        0x0400: 'ABSTRACT',
        0x0800: 'STRICTFP'
    }

    @staticmethod
    def op_id(op_id):
        '''
        Returns the name of the given OP Code
        :param op_id: OP Code
        :return: Name of the OP Code
        '''
        return StreamCodeDebug.OP_CODES.get(op_id, 'UNKNOWN_OP')

    @staticmethod
    def type_code(type_id):
        '''
        Returns the name of the given Type Code
        :param type_id: Type code
        :return: Name of the type code
        '''
        return StreamCodeDebug.TYPE_CODES.get(type_id, 'UNKNOWN_TYPE')

    @staticmethod
    def flags(flags):
        '''
        Returns the names of the class description flags found in the given
        integer
        :param flags: A class description flag entry
        :return: The flags names as a single string
        '''
        flag_names = [name for mask,
                      name in StreamCodeDebug.FLAG_NAMES.items() if flags & mask]
        return ', '.join(flag_names) if flag_names else 'NO_FLAGS'

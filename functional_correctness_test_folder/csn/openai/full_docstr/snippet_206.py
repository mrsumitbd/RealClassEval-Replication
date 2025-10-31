
class StreamCodeDebug:
    '''
    Codes utility methods
    '''
    _OP_CODES = {
        0x01: 'OP_ADD',
        0x02: 'OP_SUB',
        0x03: 'OP_MUL',
        0x04: 'OP_DIV',
        0x05: 'OP_LOAD',
        0x06: 'OP_STORE',
        0x07: 'OP_CALL',
        0x08: 'OP_RET',
        0x09: 'OP_JMP',
        0x0A: 'OP_JZ',
        0x0B: 'OP_JNZ',
        0x0C: 'OP_PUSH',
        0x0D: 'OP_POP',
    }

    _TYPE_CODES = {
        0x01: 'TYPE_INT',
        0x02: 'TYPE_FLOAT',
        0x03: 'TYPE_STRING',
        0x04: 'TYPE_BOOL',
        0x05: 'TYPE_OBJECT',
        0x06: 'TYPE_ARRAY',
    }

    _FLAGS = {
        0x01: 'PUBLIC',
        0x02: 'PRIVATE',
        0x04: 'PROTECTED',
        0x08: 'STATIC',
        0x10: 'FINAL',
        0x20: 'ABSTRACT',
        0x40: 'INTERFACE',
        0x80: 'ENUM',
    }

    @staticmethod
    def op_id(op_id):
        '''
        Returns the name of the given OP Code
        :param op_id: OP Code
        :return: Name of the OP Code
        '''
        return StreamCodeDebug._OP_CODES.get(op_id, f'UNKNOWN_OP_{op_id}')

    @staticmethod
    def type_code(type_id):
        '''
        Returns the name of the given Type Code
        :param type_id: Type code
        :return: Name of the type code
        '''
        return StreamCodeDebug._TYPE_CODES.get(type_id, f'UNKNOWN_TYPE_{type_id}')

    @staticmethod
    def flags(flags):
        '''
        Returns the names of the class description flags found in the given
        integer
        :param flags: A class description flag entry
        :return: The flags names as a single string
        '''
        names = []
        for bit, name in sorted(StreamCodeDebug._FLAGS.items()):
            if flags & bit:
                names.append(name)
        return ', '.join(names) if names else 'NO_FLAGS'

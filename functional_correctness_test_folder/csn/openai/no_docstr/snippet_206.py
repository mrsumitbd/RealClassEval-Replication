class StreamCodeDebug:
    _op_map = {
        0: 'NOP',
        1: 'LOAD',
        2: 'STORE',
        3: 'ADD',
        4: 'SUB',
        5: 'MUL',
        6: 'DIV',
        7: 'JMP',
        8: 'JZ',
        9: 'CALL',
        10: 'RET',
    }

    _type_map = {
        0: 'int',
        1: 'float',
        2: 'str',
        3: 'bool',
        4: 'list',
        5: 'dict',
    }

    _flag_map = {
        0x01: 'READ',
        0x02: 'WRITE',
        0x04: 'EXECUTE',
        0x08: 'DEBUG',
        0x10: 'HIDDEN',
    }

    @staticmethod
    def op_id(op_id):
        return StreamCodeDebug._op_map.get(op_id, f'UNKNOWN_OP_{op_id}')

    @staticmethod
    def type_code(type_id):
        return StreamCodeDebug._type_map.get(type_id, f'UNKNOWN_TYPE_{type_id}')

    @staticmethod
    def flags(flags):
        names = [name for bit, name in StreamCodeDebug._flag_map.items()
                 if flags & bit]
        return '|'.join(names) if names else 'NONE'

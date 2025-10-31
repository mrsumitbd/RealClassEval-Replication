
class StreamCodeDebug:
    '''
    Codes utility methods
    '''
    @staticmethod
    def op_id(op_id):
        '''
        Returns the name of the given OP Code
        :param op_id: OP Code
        :return: Name of the OP Code
        '''
        op_codes = {
            0: 'OP_END',
            1: 'OP_NOP',
            2: 'OP_BREAKPOINT',
            # Add more OP codes as needed
        }
        return op_codes.get(op_id, 'UNKNOWN_OP_CODE')

    @staticmethod
    def type_code(type_id):
        '''
        Returns the name of the given Type Code
        :param type_id: Type code
        :return: Name of the type code
        '''
        type_codes = {
            0: 'TYPE_VOID',
            1: 'TYPE_BOOLEAN',
            2: 'TYPE_CHAR',
            # Add more type codes as needed
        }
        return type_codes.get(type_id, 'UNKNOWN_TYPE_CODE')

    @staticmethod
    def flags(flags):
        '''
        Returns the names of the class description flags found in the given
        integer
        :param flags: A class description flag entry
        :return: The flags names as a single string
        '''
        flag_names = []
        flag_values = {
            0x0001: 'ACC_PUBLIC',
            0x0010: 'ACC_FINAL',
            0x0020: 'ACC_SUPER',
            # Add more flags as needed
        }
        for flag, name in flag_values.items():
            if flags & flag:
                flag_names.append(name)
        return ' | '.join(flag_names) if flag_names else 'NO_FLAGS'

class StreamCodeDebug:
    """
    Codes utility methods
    """

    @staticmethod
    def op_id(op_id):
        """
        Returns the name of the given OP Code
        :param op_id: OP Code
        :return: Name of the OP Code
        """
        try:
            return TerminalCode(op_id).name
        except ValueError:
            return '<unknown TC:{0}>'.format(op_id)

    @staticmethod
    def type_code(type_id):
        """
        Returns the name of the given Type Code
        :param type_id: Type code
        :return: Name of the type code
        """
        try:
            return TypeCode(type_id).name
        except ValueError:
            return '<unknown TypeCode:{0}>'.format(type_id)

    @staticmethod
    def flags(flags):
        """
        Returns the names of the class description flags found in the given
        integer

        :param flags: A class description flag entry
        :return: The flags names as a single string
        """
        names = sorted((key.name for key in ClassDescFlags if key & flags))
        return ', '.join(names)
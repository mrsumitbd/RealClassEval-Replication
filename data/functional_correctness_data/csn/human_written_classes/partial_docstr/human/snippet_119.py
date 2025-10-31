class EvmInstruction:
    """Model to hold the information of the disassembly."""

    def __init__(self, address, op_code, argument=None):
        self.address = address
        self.op_code = op_code
        self.argument = argument

    def to_dict(self) -> dict:
        """

        :return:
        """
        result = {'address': self.address, 'opcode': self.op_code}
        if self.argument:
            result['argument'] = self.argument
        return result
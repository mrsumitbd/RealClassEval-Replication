
class StreamCodeDebug:

    @staticmethod
    def op_id(op_id):
        return f"Operation ID: {op_id}"

    @staticmethod
    def type_code(type_id):
        return f"Type Code: {type_id}"

    @staticmethod
    def flags(flags):
        if isinstance(flags, int):
            return f"Flags: {bin(flags)}"
        return f"Flags: {flags}"

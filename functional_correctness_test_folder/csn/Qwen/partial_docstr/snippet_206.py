
class StreamCodeDebug:

    @staticmethod
    def op_id(op_id):
        # Assuming op_id is a dictionary mapping operation IDs to their names
        op_id_map = {
            0: "OP_NOP",
            1: "OP_ADD",
            2: "OP_SUB",
            3: "OP_MUL",
            4: "OP_DIV"
        }
        return op_id_map.get(op_id, "UNKNOWN_OP")

    @staticmethod
    def type_code(type_id):
        # Assuming type_id is a dictionary mapping type IDs to their names
        type_id_map = {
            0: "TYPE_INT",
            1: "TYPE_FLOAT",
            2: "TYPE_STRING",
            3: "TYPE_BOOL",
            4: "TYPE_OBJECT"
        }
        return type_id_map.get(type_id, "UNKNOWN_TYPE")

    @staticmethod
    def flags(flags):
        # Assuming flags are bit flags and each bit represents a different flag
        flag_names = {
            1: "FLAG_PUBLIC",
            2: "FLAG_PRIVATE",
            4: "FLAG_PROTECTED",
            8: "FLAG_STATIC",
            16: "FLAG_FINAL"
        }
        active_flags = [name for bit,
                        name in flag_names.items() if flags & bit]
        return " | ".join(active_flags) if active_flags else "NO_FLAGS"

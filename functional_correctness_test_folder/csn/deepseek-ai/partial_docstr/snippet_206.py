
class StreamCodeDebug:

    @staticmethod
    def op_id(op_id):
        op_names = {
            0x00: "STREAM_END",
            0x01: "STREAM_NULL",
            0x02: "STREAM_BOOLEAN",
            0x03: "STREAM_INTEGER",
            0x04: "STREAM_FLOAT",
            0x05: "STREAM_STRING",
            0x06: "STREAM_BYTES",
            0x07: "STREAM_LIST",
            0x08: "STREAM_TUPLE",
            0x09: "STREAM_DICT",
            0x0A: "STREAM_OBJECT",
            0x0B: "STREAM_REFERENCE",
            0x0C: "STREAM_RECURSIVE",
        }
        return op_names.get(op_id, f"UNKNOWN_OP_ID_{op_id:02X}")

    @staticmethod
    def type_code(type_id):
        type_names = {
            0x00: "TYPE_NULL",
            0x01: "TYPE_BOOLEAN",
            0x02: "TYPE_INTEGER",
            0x03: "TYPE_FLOAT",
            0x04: "TYPE_STRING",
            0x05: "TYPE_BYTES",
            0x06: "TYPE_LIST",
            0x07: "TYPE_TUPLE",
            0x08: "TYPE_DICT",
            0x09: "TYPE_OBJECT",
        }
        return type_names.get(type_id, f"UNKNOWN_TYPE_{type_id:02X}")

    @staticmethod
    def flags(flags):
        flag_names = {
            0x01: "FLAG_SERIALIZABLE",
            0x02: "FLAG_EXTERNALIZABLE",
            0x04: "FLAG_CUSTOM_SERIALIZED",
            0x08: "FLAG_BLOCK_DATA",
        }
        active_flags = []
        for flag, name in flag_names.items():
            if flags & flag:
                active_flags.append(name)
        return ", ".join(active_flags) if active_flags else "NO_FLAGS"

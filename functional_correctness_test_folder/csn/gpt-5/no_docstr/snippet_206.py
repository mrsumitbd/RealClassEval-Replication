class StreamCodeDebug:

    @staticmethod
    def op_id(op_id):
        from enum import Enum, IntEnum, Flag, IntFlag
        if op_id is None:
            return "UNKNOWN"
        # Enum-like
        if isinstance(op_id, (Enum, IntEnum, Flag, IntFlag)):
            try:
                name = op_id.name
            except Exception:
                name = None
            try:
                value = op_id.value
            except Exception:
                value = None
            if name is not None and value is not None:
                return f"{name}({value})"
            return str(op_id)
        # Integer opcode
        if isinstance(op_id, int):
            return f"{op_id} (0x{op_id:02X})"
        # Callable/class types
        if isinstance(op_id, type):
            return op_id.__name__
        return str(op_id)

    @staticmethod
    def type_code(type_id):
        from enum import Enum, IntEnum, Flag, IntFlag
        if type_id is None:
            return "unknown"
        # If it's a Python type
        if isinstance(type_id, type):
            return type_id.__name__
        # Enum-like
        if isinstance(type_id, (Enum, IntEnum, Flag, IntFlag)):
            try:
                name = type_id.name
            except Exception:
                name = None
            try:
                value = type_id.value
            except Exception:
                value = None
            if name is not None and value is not None:
                return f"{name}({value})"
            return str(type_id)
        # Integer type code
        if isinstance(type_id, int):
            return f"{type_id} (0x{type_id:02X})"
        return str(type_id)

    @staticmethod
    def flags(flags):
        from enum import Flag, IntFlag
        # None
        if flags is None:
            return "0"
        # Enum flags
        if isinstance(flags, (Flag, IntFlag)):
            return str(flags)
        # Integer bitfield
        if isinstance(flags, int):
            if flags == 0:
                return "0x00"
            bit_positions = [str(i) for i in range(
                flags.bit_length()) if (flags >> i) & 1]
            bits_desc = ",".join(bit_positions)
            return f"0x{flags:02X} (bits:{bits_desc})"
        # Mapping of name -> mask
        if isinstance(flags, dict):
            set_names = []
            for name, mask in flags.items():
                try:
                    if mask and isinstance(mask, int) and (mask & mask - 1) == 0:
                        # single-bit mask
                        set_names.append(name)
                    elif isinstance(mask, int) and mask != 0:
                        set_names.append(name)
                except Exception:
                    continue
            return "|".join(sorted(set_names)) if set_names else "0"
        # Iterable of flag names
        try:
            iter(flags)  # check iterability
            if isinstance(flags, (str, bytes)):
                return str(flags)
            names = [str(x) for x in flags]
            return "|".join(names) if names else "0"
        except Exception:
            pass
        return str(flags)

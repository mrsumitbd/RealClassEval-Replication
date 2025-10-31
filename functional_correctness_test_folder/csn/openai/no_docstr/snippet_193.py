
class CkClass:
    # Default mappings for flags and state.  Sub‑classes can override.
    FLAGS_MAP = {
        0x01: "READ",
        0x02: "WRITE",
        0x04: "EXECUTE",
    }
    STATE_MAP = {
        0: "UNKNOWN",
        1: "ACTIVE",
        2: "INACTIVE",
        3: "ERROR",
    }

    def flags2text(self):
        """
        Convert the integer bitmask stored in `self.flags` into a comma‑separated
        string of flag names.  If `self.flags` is not an integer or is missing,
        an empty string is returned.
        """
        flags = getattr(self, "flags", 0)
        if not isinstance(flags, int):
            return ""
        names = [name for bit, name in self.FLAGS_MAP.items() if flags & bit]
        return ", ".join(names)

    def state2text(self):
        """
        Convert the value stored in `self.state` into a human‑readable string.
        If the state is not present in STATE_MAP, its raw value is returned as a
        string.
        """
        state = getattr(self, "state", None)
        return self.STATE_MAP.get(state, str(state))

    def to_dict(self):
        """
        Return a dictionary representation of the instance.  All public
        attributes (those not starting with an underscore) are included.  The
        textual representations of flags and state are added under the keys
        'flags_text' and 'state_text'.
        """
        data = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        data["flags_text"] = self.flags2text()
        data["state_text"] = self.state2text()
        return data

    def __str__(self):
        """
        Return a concise string representation of the instance.  It uses the
        dictionary representation for readability.
        """
        return f"{self.__class__.__name__}({self.to_dict()})"

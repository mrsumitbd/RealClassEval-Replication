
import json


class CkClass:
    # Default flag and state mappings – subclasses may override
    FLAG_MAP = {
        0x01: "READ",
        0x02: "WRITE",
        0x04: "EXECUTE",
    }
    STATE_MAP = {
        0: "UNKNOWN",
        1: "ACTIVE",
        2: "INACTIVE",
    }

    def flags2text(self):
        """
        Convert a bitmask stored in ``self.flags`` into a comma‑separated
        string of flag names.  If ``self.flags`` is missing or not an int,
        an empty string is returned.
        """
        flags = getattr(self, "flags", 0)
        if not isinstance(flags, int):
            return ""
        names = [name for bit, name in self.FLAG_MAP.items() if flags & bit]
        return ", ".join(names)

    def state2text(self):
        """
        Convert the integer stored in ``self.state`` into a human‑readable
        string using ``self.STATE_MAP``.  If the state is unknown, the
        integer value is returned as a string.
        """
        state = getattr(self, "state", None)
        if state is None:
            return ""
        return self.STATE_MAP.get(state, str(state))

    def to_dict(self):
        """
        Return a dictionary containing all public attributes of the instance.
        Attributes whose names start with an underscore are omitted.
        """
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def __str__(self):
        """
        Return a pretty‑printed JSON representation of the instance.
        """
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)

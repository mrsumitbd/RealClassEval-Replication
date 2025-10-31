
class CkClass:
    def __init__(self, flags=0, state=0):
        self.flags = flags  # integer bitmask
        self.state = state  # integer code

    FLAG_MAP = {
        1: "ENABLED",
        2: "VISIBLE",
        4: "LOCKED",
        8: "ARCHIVED",
        16: "DELETED"
    }

    STATE_MAP = {
        0: "NEW",
        1: "ACTIVE",
        2: "SUSPENDED",
        3: "CLOSED"
    }

    def flags2text(self):
        if self.flags == 0:
            return "NONE"
        names = []
        for bit, name in sorted(self.FLAG_MAP.items()):
            if self.flags & bit:
                names.append(name)
        return "|".join(names) if names else "NONE"

    def state2text(self):
        return self.STATE_MAP.get(self.state, f"UNKNOWN({self.state})")

    def to_dict(self):
        return {
            "flags": self.flags,
            "flags_text": self.flags2text(),
            "state": self.state,
            "state_text": self.state2text()
        }

    def __str__(self):
        return f"CkClass(flags={self.flags} [{self.flags2text()}], state={self.state} [{self.state2text()}])"


class CkClass:
    FLAGS_MAP = {
        0x01: "FLAG_A",
        0x02: "FLAG_B",
        0x04: "FLAG_C",
        0x08: "FLAG_D",
        0x10: "FLAG_E",
    }

    STATE_MAP = {
        0: "INIT",
        1: "RUNNING",
        2: "STOPPED",
        3: "ERROR",
    }

    def __init__(self, flags=0, state=0, **kwargs):
        self.flags = flags
        self.state = state
        for k, v in kwargs.items():
            setattr(self, k, v)

    def flags2text(self):
        if self.flags == 0:
            return "NONE"
        result = []
        for bit, name in sorted(self.FLAGS_MAP.items()):
            if self.flags & bit:
                result.append(name)
        return "|".join(result) if result else "UNKNOWN"

    def state2text(self):
        return self.STATE_MAP.get(self.state, f"UNKNOWN({self.state})")

    def to_dict(self):
        d = self.__dict__.copy()
        return d

    def __str__(self):
        d = self.to_dict()
        d['flags'] = self.flags2text()
        d['state'] = self.state2text()
        items = [f"{k}={v}" for k, v in d.items()]
        return f"CkClass({', '.join(items)})"

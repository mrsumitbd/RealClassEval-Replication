
class CkClass:

    def flags2text(self):
        return "Flags in text format"

    def state2text(self):
        return "State in text format"

    def to_dict(self):
        return {
            'flags': self.flags2text(),
            'state': self.state2text()
        }

    def __str__(self):
        return f"CkClass(flags={self.flags2text()}, state={self.state2text()})"

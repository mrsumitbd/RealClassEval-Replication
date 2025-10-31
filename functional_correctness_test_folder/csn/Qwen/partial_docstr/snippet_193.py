
class CkClass:

    def flags2text(self):
        return "Flags converted to text"

    def state2text(self):
        return "State converted to text"

    def to_dict(self):
        return {
            'flags': self.flags2text(),
            'state': self.state2text()
        }

    def __str__(self):
        return f"CkClass(flags={self.flags2text()}, state={self.state2text()})"

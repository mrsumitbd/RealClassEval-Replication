
class CkClass:

    def flags2text(self):
        return "Flags text representation"

    def state2text(self):
        return "State text representation"

    def to_dict(self):
        return {
            'flags': self.flags2text(),
            'state': self.state2text()
        }

    def __str__(self):
        return f"CkClass(flags={self.flags2text()}, state={self.state2text()})"

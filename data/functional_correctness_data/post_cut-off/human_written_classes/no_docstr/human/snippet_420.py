from pprint import pformat
from dataclasses import dataclass

@dataclass
class Edit:
    filename: str
    before: str
    after: str

    def __str__(self):
        return f'{self.filename}\nBefore:\n{pformat(self.before)}\nAfter:\n{pformat(self.after)}\n'

    def __repr__(self):
        return str(self)
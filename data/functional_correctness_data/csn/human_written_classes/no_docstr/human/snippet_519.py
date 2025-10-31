class CodeBase:
    co_code: bytes
    co_name: str
    co_filename: str
    co_firstlineno: int

    def __len__(self) -> int:
        return len(self.co_code)

    def __getitem__(self, i) -> int:
        op = self.co_code[i]
        if isinstance(op, str):
            op = ord(op)
        return op

    def __repr__(self) -> str:
        msg = f'<{self.__class__.__name__} code object {self.co_name} at {hex(id(self))}, file {self.co_filename}>'
        if hasattr(self, 'co_firstlineno'):
            msg += f', line {self.co_firstlineno}'
        return msg
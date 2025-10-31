class _BaseReply:

    def __init__(self, data):
        self.ipc_data = data
        for member in self.__class__._members:
            value = data.get(member[0], None)
            if value is not None:
                setattr(self, member[0], member[1](value))
            else:
                setattr(self, member[0], None)

    @classmethod
    def _parse_list(cls, data):
        return [cls(d) for d in data]
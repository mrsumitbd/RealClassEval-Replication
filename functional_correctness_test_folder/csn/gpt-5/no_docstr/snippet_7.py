class RecordLevel:

    def __init__(self, name, no, icon):
        self.name = name
        self.no = no
        self.icon = icon

    def __repr__(self):
        return f"RecordLevel(name={self.name!r}, no={self.no!r}, icon={self.icon!r})"

    def __format__(self, spec):
        if not spec:
            return repr(self)
        if spec in ('name', 'n'):
            return format(self.name, '')
        if spec in ('no', 'd'):
            return format(self.no, '')
        if spec in ('icon', 'i'):
            return format(self.icon, '')
        if '{' in spec and '}' in spec:
            try:
                return spec.format(name=self.name, no=self.no, icon=self.icon)
            except Exception:
                pass
        return format(repr(self), spec)

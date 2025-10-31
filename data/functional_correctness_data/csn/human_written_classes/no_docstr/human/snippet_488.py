class Rule:

    def __init__(self, klass: str, **kw: str) -> None:
        self.klass = klass
        self.kw = '; '.join([k.replace('_', '-') + ': ' + kw[k] for k in sorted(kw.keys())]).strip()
        self.kwl = [(k.replace('_', '-'), kw[k][1:]) for k in sorted(kw.keys())]

    def __str__(self) -> str:
        return '%s { %s; }' % (self.klass, self.kw)
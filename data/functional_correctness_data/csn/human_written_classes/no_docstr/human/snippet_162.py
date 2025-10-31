class CSSTerminalFunction:

    def __init__(self, name, params) -> None:
        self.name = name
        self.params = [param if isinstance(param, str) else str(param) for param in params]

    def __repr__(self) -> str:
        return '<CSS function: {}({})>'.format(self.name, ', '.join(self.params))
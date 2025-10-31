class Log:

    def __init__(self) -> None:
        self.level = None

    def to_capabilities(self) -> dict:
        if self.level:
            return {'log': {'level': self.level}}
        return {}
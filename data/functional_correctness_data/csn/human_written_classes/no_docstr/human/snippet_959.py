class Issue:

    def __init__(self, type: str, description: str, context: dict={}) -> None:
        self.type = type
        self.description = description
        self.context = context

    def as_data(self) -> dict:
        return {'type': self.type, 'context': self.context}
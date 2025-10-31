class ToDictWrapper:

    def __init__(self, tx):
        self.tx = tx

    def __eq__(self, other):
        return self.tx.id == other.tx.id

    def __hash__(self):
        return hash(self.tx.id)
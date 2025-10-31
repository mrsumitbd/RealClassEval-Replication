class Price:

    def __init__(self, value):
        self.value = float(value)
        self.token_address = None
        self.token_symbol = None

    def as_dict(self):
        result = {'value': self.value}
        if self.token_address:
            result['tokenAddress'] = self.token_address
        if self.token_symbol:
            result['tokenSymbol'] = self.token_symbol
        return result
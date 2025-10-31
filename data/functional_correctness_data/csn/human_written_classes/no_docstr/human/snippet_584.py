class DataRule:

    def __init__(self, endpoint, slave_ids, function_codes, addresses):
        self.endpoint = endpoint
        self.slave_ids = slave_ids
        self.function_codes = function_codes
        self.addresses = addresses

    def match(self, slave_id, function_code, address):

        def matches(values, v):
            return values is None or v in values
        return matches(self.slave_ids, slave_id) and matches(self.function_codes, function_code) and matches(self.addresses, address)
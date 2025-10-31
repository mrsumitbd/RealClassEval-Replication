class Map:

    def __init__(self):
        self._rules = []

    def add_rule(self, endpoint, slave_ids, function_codes, addresses):
        self._rules.append(DataRule(endpoint, slave_ids, function_codes, addresses))

    def match(self, slave_id, function_code, address):
        for rule in self._rules:
            if rule.match(slave_id, function_code, address):
                return rule.endpoint
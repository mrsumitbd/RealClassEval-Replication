class ReplaceSequence:

    def __init__(self):
        self.replacements = []

    def create(self, first_pattern, replace_with=None):
        result = StringReplacement(first_pattern, replace_with or '')
        self.replacements.append(result)
        return self

    def append(self, pattern, replace_with=None):
        return self.create(pattern, replace_with)

    def replace_all(self, string):
        if not string:
            return ''
        mutated_string = string
        for itm in self.replacements:
            mutated_string = itm.replace_all(mutated_string)
        return mutated_string
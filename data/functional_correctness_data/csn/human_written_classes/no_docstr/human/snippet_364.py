class StringReplacement:

    def __init__(self, pattern, replace_with):
        self.pattern = pattern
        self.replace_with = replace_with

    def replace_all(self, string):
        if not string:
            return ''
        return string.replace(self.pattern, self.replace_with)
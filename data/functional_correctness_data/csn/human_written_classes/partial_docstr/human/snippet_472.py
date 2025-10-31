class CompoundRule:
    """ Class to match compound rules """

    def __init__(self, compound):
        self.compound = compound
        self.flags = {}
        for flag in self.compound:
            if flag != '?' and flag != '*':
                self.flags[flag] = []

    def add_flag_values(self, entry, flag):
        """ Adds flag value to applicable compounds """
        if flag in self.flags:
            self.flags[flag].append(entry)

    def get_regex(self):
        """ Generates and returns compound regular expression """
        regex = ''
        for flag in self.compound:
            if flag == '?' or flag == '*':
                regex += flag
            else:
                regex += '(' + '|'.join(self.flags[flag]) + ')'
        return regex
import re

class AFF:
    """ Class to match AFF file and rules """

    def __init__(self, in_file):
        self.affix_rules = {}
        self.compound_rules = []
        self.rep_table = {}
        self.key = []
        self.no_suggest_flag = None
        self.only_in_compound_flag = None
        self.compound_flags = ''
        self.min_len_compound_words = 1
        self.lines = file_to_list(in_file)
        self.__parse_rules()

    def __parse_rules(self):
        lines = self.lines
        i = 0
        while i < len(lines):
            line = lines[i]
            parts = re.split('\\s+', line)
            opt = parts[0]
            flag = parts[1]
            if opt == 'PFX' or opt == 'SFX':
                combine = parts[2]
                num_entries = int(parts[3])
                j = 0
                while j < num_entries:
                    i += 1
                    line = lines[i]
                    parts = re.split('\\s+', line)
                    char_to_strip = parts[2]
                    affix = parts[3]
                    condition = parts[4]
                    if flag not in self.affix_rules:
                        self.affix_rules[flag] = []
                    self.affix_rules[flag].append(AffixRule(flag, opt, combine, char_to_strip, affix, condition))
                    j += 1
            elif opt == 'REP':
                num_entries = int(parts[1])
                j = 0
                while j < num_entries:
                    i += 1
                    line = lines[i]
                    parts = re.split('\\s+', line)
                    self.rep_table[parts[1]] = parts[2]
                    j += 1
            elif opt == 'NOSUGGEST':
                self.no_suggest_flag = flag
            elif opt == 'COMPOUNDMIN':
                self.min_len_compound_words = int(flag)
            elif opt == 'ONLYINCOMPOUND':
                self.only_in_compound_flag = flag
            elif opt == 'COMPOUNDRULE':
                num_entries = int(parts[1])
                j = 0
                while j < num_entries:
                    i += 1
                    line = lines[i]
                    parts = re.split('\\s+', line)
                    compound = parts[1]
                    for comp in compound:
                        if comp != '*' and comp != '?' and (comp not in self.compound_flags):
                            self.compound_flags += comp
                    self.compound_rules.append(CompoundRule(compound))
                    j += 1
            i += 1
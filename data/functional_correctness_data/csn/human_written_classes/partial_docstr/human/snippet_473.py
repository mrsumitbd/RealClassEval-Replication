import json

class DICT:

    def __init__(self, dict_file, aff, json_format, key, generate_compounds, generate_rep_table, is_pretty):
        self.lines = file_to_list(dict_file)
        self.aff = aff
        self.words = {}
        self.num_words = 0
        self.keys = []
        self.format = json_format
        self.key = key
        self.compounds = generate_compounds
        self.regex_compounds = []
        self.rep_table = generate_rep_table
        self.pretty = is_pretty
        self.__parse_dict()

    def generate_json(self, out_file, gzip_set):
        result = None
        new_line = '\n' if self.pretty else ''
        tab = '\t' if self.pretty else ''
        result = '{'
        result += new_line + tab + '"numWords": ' + str(self.num_words) + ','
        if self.key:
            result += new_line + tab + '"keys": ["' + '","'.join(self.keys) + '"],'
        if self.compounds:
            result += new_line + tab + '"compounds": ["' + '","'.join(self.regex_compounds) + '"],'
        if self.rep_table:
            result += new_line + tab + '"repTable": ' + json.dumps(self.aff.rep_table, separators=(',', ':'))
        result += new_line + tab + '"words": {'
        i = 0
        for word in self.words:
            val = self.words[word]
            comma = ',' if i < len(self.words) - 1 else ''
            result += new_line + tab + tab + '"' + word + '":[' + ','.join(val) + ']' + comma
            i += 1
        result += new_line + tab + '}'
        result += new_line + '}'
        if gzip_set:
            out_file.write(bytes(result, 'UTF-8'))
        else:
            out_file.write(result)

    def __parse_dict(self):
        """ Parses dictionary with according rules """
        i = 0
        lines = self.lines
        for line in lines:
            line = line.split('/')
            word = line[0]
            flags = line[1] if len(line) > 1 else None
            self.num_words += 1
            if flags != None:
                for flag in flags:
                    if flag in self.aff.compound_flags or flag == self.aff.only_in_compound_flag:
                        for rule in self.aff.compound_rules:
                            rule.add_flag_values(word, flag)
                    elif self.aff.no_suggest_flag == flag:
                        pass
                    else:
                        affix_rule_entries = self.aff.affix_rules[flag]
                        for i in range(len(affix_rule_entries)):
                            rule = affix_rule_entries[i]
                            if rule.meets_condition(word):
                                if word not in self.words:
                                    self.words[word] = []
                                self.num_words += 1
                                if self.format == 'addsub':
                                    add_sub = rule.generate_add_sub()
                                    if add_sub not in self.keys:
                                        self.keys.append(add_sub)
                                    if self.key:
                                        self.words[word].append(str(self.keys.index(add_sub)))
                                    else:
                                        self.words[word].append(rule.generate_add_sub())
                                else:
                                    self.words[word].append(rule.create_derivative(word))
            else:
                self.words[word] = []
        for rule in self.aff.compound_rules:
            self.regex_compounds.append(rule.get_regex())
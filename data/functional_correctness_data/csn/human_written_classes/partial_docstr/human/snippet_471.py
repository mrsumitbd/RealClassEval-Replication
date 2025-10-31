import re

class AffixRule:
    """ Class matching affix rule defined in Hunspell .aff files """

    def __init__(self, flag, opt, combine, char_to_strip, affix, condition):
        self.flag = flag
        self.opt = opt
        self.combine = True if combine == 'Y' else False
        self.char_to_strip = '' if char_to_strip == '0' else char_to_strip
        self.affix = affix
        self.condition = '.' if condition == ',' else re.compile(condition + '$')

    def generate_add_sub(self):
        """ Generates prefixes/suffixes in a short form to parse and remove some redundancy """
        affix_type = 'p:' if self.opt == 'PFX' else 's:'
        remove_char = '-' + self.char_to_strip if self.char_to_strip != '' else ''
        return affix_type + remove_char + '+' + self.affix

    def meets_condition(self, word):
        """ Checks if word meets conditionr requirements defined in affix rule """
        if self.condition.search(word):
            return True
        return False

    def create_derivative(self, word):
        """ Creates derivative of (base) word by adding any affixes that apply """
        result = None
        if self.char_to_strip != '':
            if self.opt == 'PFX':
                result = word[len(self.char_to_strip):len(word)]
                result = self.affix + result
            else:
                result = word[0:len(word) - len(self.char_to_strip)]
                result = result + self.affix
        elif self.opt == 'PFX':
            result = self.affix + word
        else:
            result = word + self.affix
        return result
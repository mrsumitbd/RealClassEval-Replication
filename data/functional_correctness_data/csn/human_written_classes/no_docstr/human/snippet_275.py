class Word:

    def __init__(self, word, senses=[]):
        self.word = word
        self.senses = senses

    def __str__(self):
        return self.word + ' ' + ','.join([sense.tag for sense in self.senses]) + ','

    def add_sense(self, sense):
        self.senses.append(sense)

    def has_tag(self, tag) -> bool:
        for sense in self.senses:
            if sense.tag == tag:
                return True
        return False
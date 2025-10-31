class parsed_date:

    def __init__(self):
        self.is_range = False
        self.predicted_date = dict()

    def get_printable_version(self):
        return self.predicted_date

    def equals(self, p):
        for i in self.predicted_date.keys():
            if i not in p.predicted_date.keys():
                return False
            if p.predicted_date[i] != self.predicted_date[i]:
                return False
        return True
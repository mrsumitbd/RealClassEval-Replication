class parsed_interval:

    def __init__(self):
        self.begin_interval = parsed_date()
        self.end_interval = parsed_date()
        self.predicted_date_certainty = dict()

    def equals(self, p):
        if not self.begin_interval.equals(p.begin_interval):
            return False
        if not self.end_interval.equals(p.end_interval):
            return False
        return True

    def print_interval(self):
        stres = 'begin: ' + str(self.begin_interval.get_printable_version()) + ' end: ' + str(self.end_interval.get_printable_version())
        print(stres)
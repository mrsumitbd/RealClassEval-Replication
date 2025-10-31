from collections import defaultdict

class realign:

    def __init__(self):
        self.sequence = ''
        self.precursors = defaultdict(isomir)
        self.score = []
        self.best_hits = []

    def set_precursor(self, precursor, isomir):
        self.precursors[precursor] = isomir

    def remove_precursor(self, precursor):
        del self.precursors[precursor]
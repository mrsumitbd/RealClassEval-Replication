from collections import Counter
import pickle

class Stats:

    def __init__(self):
        self.perfile = {}
        self.fdbars = {}
        self.fsamplehits = Counter()
        self.fbarhits = Counter()
        self.fmisses = Counter()

    def fill_from_pickle(self, pkl, handle):
        with open(pkl, 'rb') as infile:
            filestats, samplestats = pickle.load(infile)
        self.perfile[handle] += filestats
        samplehits, barhits, misses, dbars = samplestats
        self.fsamplehits.update(samplehits)
        self.fbarhits.update(barhits)
        self.fmisses.update(misses)
        self.fdbars.update(dbars)
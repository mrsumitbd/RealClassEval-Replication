from ase.units import mol, fs
import numpy as np

class CoordinationCount:

    def __init__(self, dyn, calc, cutoff, maxc=10, logfile=None):
        self.dyn = dyn
        self.calc = calc
        self.cutoff = cutoff
        self.maxc = maxc
        self.hist = np.zeros(maxc, dtype=int)
        self.navg = 0
        self.logfile = logfile
        if isinstance(logfile, str):
            self.logfile = open(logfile, 'w')
        self.fmt = '{0:.2f}'
        for i in range(maxc + 1):
            self.fmt += ' {{{0}}}'.format(i + 1)
        self.fmt += '\n'

    def __call__(self):
        c = self.calc.nl.get_coordination_numbers(self.calc.particles, self.cutoff)
        hist = np.bincount(c)
        if len(hist) < self.maxc:
            hist = np.append(hist, np.zeros(self.maxc - len(hist), dtype=int))
        self.hist += hist
        self.navg += 1
        if self.logfile is not None:
            self.hist /= self.navg
            self.hist = np.append(self.hist, np.sum(self.hist))
            self.logfile.write(self.fmt.format(self.dyn.get_time() / (1000 * fs), *self.hist))
            self.hist = np.zeros(self.maxc, dtype=int)
            self.navg = 0

    def get_hist(self):
        return self.hist / self.navg
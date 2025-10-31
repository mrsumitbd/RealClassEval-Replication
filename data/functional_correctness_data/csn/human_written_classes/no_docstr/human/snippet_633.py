import scipy.signal as sps
import numpy as np

class MorletSpec:

    def __init__(self, tsvec, sampr, freqmin=1.0, freqmax=250.0, freqstep=1.0, width=7.0, getphase=False, lfreq=None):
        self.freqmin = freqmin
        self.freqmax = freqmax
        self.freqstep = freqstep
        if lfreq is not None:
            self.f = [freq for freq in lfreq]
            self.freqmin = min(self.f)
            self.freqmax = max(self.f)
        else:
            self.f = np.arange(self.freqmin, self.freqmax + 1, self.freqstep)
        self.width = width
        self.sampr = sampr
        self.transform(tsvec, getphase)

    def plot_to_ax(self, ax_spec, dt):
        pc = ax_spec.imshow(self.TFR, aspect='auto', origin='upper', cmap=plt.get_cmap('jet'))
        return pc

    def transform(self, tsvec, getphase=False):
        sig = sps.detrend(tsvec - np.mean(tsvec))
        self.t = np.linspace(0, 1000.0 * len(sig) / self.sampr, len(sig))
        self.TFR = np.zeros((len(self.f), len(sig)))
        self.PHS = None
        if getphase:
            self.PHS = np.zeros((len(self.f), len(sig)))
            for j, freq in enumerate(self.f):
                self.TFR[j, :], self.PHS[j, :] = MorletVec(sig, self.sampr, freq, self.width, getphase=True)
        else:
            for j, freq in enumerate(self.f):
                self.TFR[j, :] = MorletVec(sig, self.sampr, freq, self.width, getphase=False)
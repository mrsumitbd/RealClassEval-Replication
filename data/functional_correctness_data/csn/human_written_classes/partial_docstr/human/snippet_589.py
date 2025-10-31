import warnings

class VqeResult:

    def __init__(self, vqe=None, params=None, circuit=None):
        self.vqe = vqe
        self.params = params
        self.circuit = circuit
        self._probs = None

    def most_common(self, n=1):
        return tuple(sorted(self.get_probs().items(), key=lambda item: -item[1]))[:n]

    @property
    def probs(self):
        """Get probabilities. This property is obsoleted. Use get_probs()."""
        warnings.warn('VqeResult.probs is obsoleted. ' + 'Use VqeResult.get_probs().', DeprecationWarning)
        return self.get_probs()

    def get_probs(self, sampler=None, rerun=None, store=True):
        """Get probabilities."""
        if rerun is None:
            rerun = sampler is not None
        if self._probs is not None and (not rerun):
            return self._probs
        if sampler is None:
            sampler = self.vqe.sampler
        if sampler is None:
            probs = expect(self.circuit.run(returns='statevector'), range(self.circuit.n_qubits))
        else:
            probs = sampler(self.circuit, range(self.circuit.n_qubits))
        if store:
            self._probs = probs
        return probs
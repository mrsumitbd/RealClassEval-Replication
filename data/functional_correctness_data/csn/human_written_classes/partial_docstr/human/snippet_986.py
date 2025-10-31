import numpy as np

class _result:
    """
    Minimal emcee.EnsembleSampler like container for chain results
    """

    def get_value(self, name, flat=False):
        v = getattr(self, name)
        if flat:
            s = list(v.shape[1:])
            s[0] = np.prod(v.shape[:2])
            return v.reshape(s)
        return v

    def get_chain(self, **kwargs):
        return self.get_value('chain', **kwargs)

    def get_log_prob(self, **kwargs):
        return self.get_value('log_prob', **kwargs)

    def get_blobs(self, **kwargs):
        return self.get_value('_blobs', **kwargs)
from bambi.terms import CommonTerm, GroupSpecificTerm, HSGPTerm, OffsetTerm, ResponseTerm
import numpy as np
from bambi.families import univariate, multivariate

class ResponseComponent:

    def __init__(self, response, spec):
        self.term = None
        self.response = response
        self.spec = spec
        self._init_response()

    def _init_response(self):
        response = self.response
        if hasattr(response.term.term.components[0], 'reference'):
            reference = response.term.term.components[0].reference
        else:
            reference = None
        if reference is not None and (not isinstance(self.spec.family, univariate.Bernoulli)):
            raise ValueError("Index notation for response is only available for 'bernoulli' family")
        if isinstance(self.spec.family, univariate.Bernoulli):
            if response.kind == 'categoric' and response.levels is None and (reference is None):
                raise ValueError("Categoric response must be binary for 'bernoulli' family.")
            if response.kind == 'numeric' and (not all(np.isin(response.design_matrix, (0, 1)))):
                raise ValueError("Numeric response must be all 0 and 1 for 'bernoulli' family.")
        self.term = ResponseTerm(response, self.spec.family)
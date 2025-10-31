from bambi.families.multivariate import MultivariateFamily
from bambi.backend.utils import get_distribution_from_likelihood, get_distribution_from_prior, get_linkinv, has_hyperprior, make_weighted_distribution, GP_KERNELS
import numpy as np
from bambi.families.univariate import Categorical, Cumulative, StoppingRatio

class InterceptTerm:
    """Representation of an intercept term in a PyMC model

    Parameters
    ----------
    term : bambi.terms.Term
        An object representing the intercept. This has `.kind == "intercept"`
    """

    def __init__(self, term):
        self.term = term

    def build(self, spec):
        dist = get_distribution_from_prior(self.term.prior)
        label = self.name
        if isinstance(spec.family, (MultivariateFamily, Categorical)):
            dims = list(spec.response_component.term.coords)
            dist = dist(label, dims=dims, **self.term.prior.args)[np.newaxis, :]
        else:
            dist = dist(label, **self.term.prior.args)
            dist = dist * np.ones((spec.response_component.term.data.shape[0],))
        return dist

    @property
    def name(self):
        if self.term.alias:
            return self.term.alias
        return self.term.name
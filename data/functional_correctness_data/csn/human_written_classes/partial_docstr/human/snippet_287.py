class ConstantComponent:
    """Constant model components

    This is a component for a target parameter that has no predictors. This could be seen as
    an intercept-only model for that parameter. For example, this is the case for sigma when
    a non-distributional Normal linear regression model is used.

    Parameters
    ----------
    name : str
        The name of the component. For example "sigma", "alpha", or "kappa".
    priors : bambi.priors.Prior
        The prior distribution for the parameter.
    spec : bambi.Model
        The Bambi model.
    """

    def __init__(self, name, prior, spec):
        self.alias = None
        self.name = name
        self.prior = prior
        self.spec = spec

    def update_priors(self, value):
        self.prior = value
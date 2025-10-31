from bambi.utils import multilinify, indentify

class Link:
    """Representation of a link function

    This object contains two main functions. One is the link function itself, the function
    that maps values in the response scale to the linear predictor, and the other is the inverse
    of the link function, that maps values of the linear predictor to the response scale.

    The great majority of users will never interact with this class unless they want to create
    a custom `Family` with a custom `Link`. This is automatically handled for all the built-in
    families.

    Parameters
    ----------
    name : str
        The name of the link function. If it is a known name, it's not necessary to pass any
        other arguments because functions are already defined internally. If not known, all of
        `link`, `linkinv` and `linkinv_backend` must be specified.
    link : function
        A function that maps the response to the linear predictor. Known as the :math:`g` function
        in GLM jargon. Does not need to be specified when `name` is a known name.
    linkinv : function
        A function that maps the linear predictor to the response. Known as the :math:`g^{-1}`
        function in GLM jargon. Does not need to be specified when `name` is a known name.
    linkinv_backend : function
        Same than `linkinv` but must be something that works with PyMC backend (i.e. it must
        work with PyTensor tensors). Does not need to be specified when `name` is a known
        name.
    """

    def __init__(self, name, link=None, linkinv=None, linkinv_backend=None):
        self.name = name
        self.link = link
        self.linkinv = linkinv
        self.linkinv_backend = linkinv_backend
        if name in LINKS:
            self.link = LINKS[name].link
            self.linkinv = LINKS[name].linkinv
        elif not link or not linkinv or (not linkinv_backend):
            raise ValueError(f"Link name '{name}' is not supported and at least one of 'link', 'linkinv' or 'linkinv_backend' are unspecified.")

    def __str__(self):
        args = [f'name: {self.name}', f'link: {self.link}', f'linkinv: {self.linkinv}']
        return f'{self.__class__.__name__}({indentify(multilinify(args))}\n)'

    def __repr__(self):
        return self.__str__()
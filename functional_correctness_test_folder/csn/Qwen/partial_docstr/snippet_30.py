
class LazyOpResult:
    '''Wrapper class around as yet un-evaluated Weld computation results
    Attributes:
        dim (int): Dimensionality of the output
        expr (WeldObject / Numpy.ndarray): The expression that needs to be
            evaluated
        weld_type (WeldType): Type of the output object
    '''

    def __init__(self, expr, weld_type, dim):
        self.expr = expr
        self.weld_type = weld_type
        self.dim = dim

    def evaluate(self, verbose=True, decode=True, passes=None, num_threads=1, apply_experimental_transforms=False):
        '''Summary
        Args:
            verbose (bool, optional): Description
            decode (bool, optional): Description
        Returns:
            TYPE: Description
        '''
        from weld.api import WeldContext, WeldConf
        conf = WeldConf()
        conf.set("weld.threads", str(num_threads))
        if apply_experimental_transforms:
            conf.set("weld.apply_experimental_transforms", "true")
        if passes:
            conf.set("weld.passes", passes)
        with WeldContext(conf=conf) as context:
            result = context.run(self.expr, self.weld_type)
        if decode:
            result = result.decode()
        if verbose:
            print("Evaluation complete.")
        return result

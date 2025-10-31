
class LazyOpResult:
    '''Wrapper class around as yet un-evaluated Weld computation results
    Attributes:
        dim (int): Dimensionality of the output
        expr (WeldObject / Numpy.ndarray): The expression that needs to be
            evaluated
        weld_type (WeldType): Type of the output object
    '''

    def __init__(self, expr, weld_type, dim):
        '''Summary
        Args:
            expr (TYPE): Description
            weld_type (TYPE): Description
            dim (TYPE): Description
        '''
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
        from weld.types import WeldVec, WeldInt, WeldFloat, WeldDouble, WeldChar, WeldLong
        from weld.encoders import NumpyArrayEncoder, NumpyArrayDecoder

        conf = WeldConf()
        conf.set("weld.threads", str(num_threads))
        if apply_experimental_transforms:
            conf.set("weld.apply_experimental_transforms", "true")

        context = WeldContext(conf)

        if passes is not None:
            context.set_passes(passes)

        encoder = NumpyArrayEncoder()
        decoder = NumpyArrayDecoder()

        encoded_expr = encoder.encode(self.expr, self.weld_type)

        if verbose:
            print("Evaluating Weld expression...")

        result = context.run(self.weld_type, encoded_expr)

        if decode:
            result = decoder.decode(result, self.weld_type)

        return result


class LazyOpResult:

    def __init__(self, expr, weld_type, dim):
        self.expr = expr
        self.weld_type = weld_type
        self.dim = dim

    def evaluate(self, verbose=True, decode=True, passes=None, num_threads=1, apply_experimental_transforms=False):
        pass

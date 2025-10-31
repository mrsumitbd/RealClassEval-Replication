import traceback
import numpy as np

class _function_wrapper:
    """
    A hack to make functions pickleable when `args` or `kwargs` are
    also included. Based on the implementation in
    `emcee <http://dan.iel.fm/emcee/>`_.

    """

    def __init__(self, func, args, kwargs, name='input'):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.name = name

    def __call__(self, x):
        try:
            return self.func(np.asarray(x).copy(), *self.args, **self.kwargs)
        except:
            print(f'Exception while calling {self.name} function:')
            print('  params:', x)
            print('  args:', self.args)
            print('  kwargs:', self.kwargs)
            print('  exception:')
            traceback.print_exc()
            raise
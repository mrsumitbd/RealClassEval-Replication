import casadi as ca

class CasadiModel:

    def __init__(self, sym, *args, **kwargs):
        self.sym = sym
        for k, v in kwargs.items():
            if k in self.__dict__.keys():
                setattr(self, k, v)
            else:
                raise ValueError('unknown argument', k)
        if ca.Importer.has_plugin('clang'):
            with_jit = True
            compiler = 'clang'
        elif ca.Importer.has_plugin('shell'):
            with_jit = True
            compiler = 'shell'
        else:
            print('WARNING; running without jit. This may result in very slow evaluation times')
            with_jit = False
            compiler = ''
        self.func_opt = {'jit': with_jit, 'compiler': compiler}

    def __repr__(self):
        s = '\n'
        for k, v in sorted(self.__dict__.items()):
            if isinstance(v, self.sym):
                s += '{:8s}({:3d}):\t{:s}\n'.format(k, v.shape[0], str(v))
        return s
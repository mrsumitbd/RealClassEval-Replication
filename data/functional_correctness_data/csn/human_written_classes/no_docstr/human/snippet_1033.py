import uuid
import sympy as sym

class ODEsys:

    def __init__(self, rhs, ny, nparams):
        self.t = sym.Symbol('t', real=True)
        self.y = tuple((sym.Symbol('y%d' % i, real=True) for i in range(ny)))
        self.p = tuple((sym.Symbol('p%d' % i, real=True) for i in range(nparams)))
        self.f = tuple(rhs(self.t, self.y, self.p))
        assert len(self.f) == len(self.y), 'f is dy/dt'
        self.j = sym.Matrix(len(self.y), 1, self.f).jacobian(self.y)
        self.uid = uuid.uuid4().hex[:10]

    def generate_sources(self, build_dir):
        self.mod_name = 'ode_c_%s' % self.uid
        idxs = list(range(len(self.f)))
        subs = {}
        subs.update({s: sym.Symbol('y[%d]' % i) for i, s in enumerate(self.y)})
        subs.update({s: sym.Symbol('p[%d]' % i) for i, s in enumerate(self.p)})
        f_exprs = ['out[%d] = %s;' % (i, sym.ccode(self.f[i].xreplace(subs))) for i in idxs]
        j_col_defs = ['realtype * const col_%d = SM_COLUMN_D(J, %d);' % (ci, ci) for ci in idxs]
        j_exprs = ['col_%d[%d] = %s;' % (ci, ri, self.j[ri, ci].xreplace(subs)) for ci in idxs for ri in idxs if self.j[ri, ci] != 0]
        ctx = dict(func='\n    '.join(f_exprs + ['return 0;']), dense_jac='\n    '.join(j_col_defs + j_exprs + ['return 0;']))
        sources = {build_dir + '/integrate_serial_%s.c' % self.uid: template_integrate_serial_c89 % ctx, build_dir + '/%s.pyx' % self.mod_name: template_integrate_serial_pyx % {'uid': self.uid}}
        for pth, content in sources.items():
            with open(pth, 'wt') as fh:
                fh.write(content)
        return list(sources.keys())
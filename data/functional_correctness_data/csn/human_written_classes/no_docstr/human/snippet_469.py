import particles
import numpy as np
from particles import state_space_models as ssms

class MinusLogLikEvaluator:

    def __init__(self, N=1000):
        self.N = N
        self.args = []
        self.lls = []

    def __call__(self, x):
        rho, sig2 = (x[0], x[1])
        if rho > 1.0 or rho < 0.0 or sig2 <= 0:
            return np.inf
        fk = ssms.Bootstrap(ssm=NeuroXp(rho=rho, sig2=sig2), data=data)
        pf = particles.SMC(fk=fk, N=self.N, qmc=True)
        pf.run()
        self.args.append(x)
        self.lls.append(pf.logLt)
        return -pf.logLt
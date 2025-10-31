import numpy as np

class MeshVertex:

    def __init__(self, r, dpdx, dpdy, dpdz, *args):
        """
        """
        nx = dpdx(r, *args)
        ny = dpdy(r, *args)
        nz = dpdz(r, *args)
        nn = np.sqrt(nx * nx + ny * ny + nz * nz)
        nx /= nn
        ny /= nn
        nz /= nn
        if nx > 0.5 or ny > 0.5:
            nn = np.sqrt(ny * ny + nx * nx)
            t1x = ny / nn
            t1y = -nx / nn
            t1z = 0.0
        else:
            nn = np.sqrt(nx * nx + nz * nz)
            t1x = -nz / nn
            t1y = 0.0
            t1z = nx / nn
        t2x = ny * t1z - nz * t1y
        t2y = nz * t1x - nx * t1z
        t2z = nx * t1y - ny * t1x
        self.r = r
        self.n = np.array((nx, ny, nz))
        self.t1 = np.array((t1x, t1y, t1z))
        self.t2 = np.array((t2x, t2y, t2z))

    def __repr__(self):
        repstr = ' r = (% 3.3f, % 3.3f, % 3.3f)\t' % (self.r[0], self.r[1], self.r[2])
        repstr += ' n = (% 3.3f, % 3.3f, % 3.3f)\t' % (self.n[0], self.n[1], self.n[2])
        repstr += 't1 = (% 3.3f, % 3.3f, % 3.3f)\t' % (self.t1[0], self.t1[1], self.t1[2])
        repstr += 't2 = (% 3.3f, % 3.3f, % 3.3f)' % (self.t2[0], self.t2[1], self.t2[2])
        return repstr
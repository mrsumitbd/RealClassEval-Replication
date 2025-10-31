from scipy import sparse
import numpy as np

class Mesh:
    """Simple mesh object that holds vertices and mesh functions."""

    def __init__(self, V, E, degree=1):
        """Initialize mesh.

        Parameters
        ----------
        V : ndarray
            nv x 2 list of coordinates
        E : ndarray
            ne x 3 list of vertices
        degree : int
            Polynomial degree, either 1 or 2

        """
        ids = np.full((E.max() + 1,), False)
        ids[E.ravel()] = True
        nv = np.sum(ids)
        if V.shape[0] != nv:
            print('fixing V and E')
            I = np.where(ids)[0]
            J = np.arange(E.max() + 1)
            J[I] = np.arange(nv)
            E = J[E]
            V = V[I, :]
        if not check_mesh(V, E):
            raise ValueError('triangles must be counter clockwise')
        self.V = V
        self.E = E
        self.X = V[:, 0]
        self.Y = V[:, 1]
        self.degree = degree
        self.nv = nv
        self.ne = E.shape[0]
        self.h = diameter(V, E)
        self.V2 = None
        self.E2 = None
        self.Edges = None
        self.newID = None
        if degree == 2:
            self.generate_quadratic()

    def generate_quadratic(self):
        """Generate a quadratic mesh."""
        if self.V2 is None:
            self.V2, self.E2, self.Edges = generate_quadratic(self.V, self.E, return_edges=True)
            self.X2 = self.V2[:, 0]
            self.Y2 = self.V2[:, 1]
            self.newID = self.nv + np.arange(self.Edges.shape[0])

    def refine(self, levels):
        """Refine the mesh.

        Parameters
        ----------
        levels : int
            Number of refinement levels.

        """
        self.V2 = None
        self.E2 = None
        self.Edges = None
        self.newID = None
        for _ in range(levels):
            self.V, self.E = refine2dtri(self.V, self.E)
        self.nv = self.V.shape[0]
        self.ne = self.E.shape[0]
        self.h = diameter(self.V, self.E)
        self.X = self.V[:, 0]
        self.Y = self.V[:, 1]
        if self.degree == 2:
            self.generate_quadratic()

    def smooth(self, maxit=10, tol=0.01):
        """Constrained Laplacian Smoothing.

        Parameters
        ----------
        maxit : int
            Iterations
        tol : float
            Convergence toleratnce measured in the maximum
            absolute distance the mesh moves (in one iteration).

        """
        nv = self.nv
        edge0 = self.E[:, [0, 0, 1, 1, 2, 2]].ravel()
        edge1 = self.E[:, [1, 2, 0, 2, 0, 1]].ravel()
        data = np.ones((edge0.shape[0],), dtype=int)
        G = sparse.coo_array((data, (edge0, edge1)), shape=(nv, nv))
        G.sum_duplicates()
        G.eliminate_zeros()
        bid = np.where(G.data == 1)[0]
        bid = np.unique(G.row[bid])
        G.data[:] = 1
        W = np.array(G.sum(axis=1)).flatten()
        Vnew = self.V.copy()
        edgelength = (Vnew[edge0, 0] - Vnew[edge1, 0]) ** 2 + (Vnew[edge0, 1] - Vnew[edge1, 1]) ** 2
        maxit = 100
        for _it in range(maxit):
            Vnew = G @ Vnew
            Vnew /= W[:, None]
            Vnew[bid, :] = self.V[bid, :]
            newedgelength = np.sqrt((Vnew[edge0, 0] - Vnew[edge1, 0]) ** 2 + (Vnew[edge0, 1] - Vnew[edge1, 1]) ** 2)
            move = np.max(np.abs(newedgelength - edgelength) / newedgelength)
            edgelength = newedgelength
            if move < tol:
                break
        self.V = Vnew
        return _it
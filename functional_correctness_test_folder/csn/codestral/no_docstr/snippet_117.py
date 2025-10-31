
class PDE:

    def __init__(self, lhs, rhs, bcs):

        self.lhs = lhs
        self.rhs = rhs
        self.bcs = bcs

    def solve(self):

        from fenics import *
        from mshr import *

        # Create mesh and define function space
        domain = Circle(Point(0, 0), 1)
        mesh = generate_mesh(domain, 64)
        V = FunctionSpace(mesh, 'P', 1)

        # Define boundary condition
        def boundary(x, on_boundary):
            return on_boundary

        bc = DirichletBC(V, Constant(0), boundary)

        # Define variational problem
        u = TrialFunction(V)
        v = TestFunction(V)
        f = Constant(-6.0)
        a = dot(grad(u), grad(v))*dx
        L = f*v*dx

        # Compute solution
        u = Function(V)
        solve(a == L, u, bc)

        return u

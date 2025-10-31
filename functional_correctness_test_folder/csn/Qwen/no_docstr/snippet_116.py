
class Solver:

    def getSolution(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        from constraint import Problem
        problem = Problem()
        for var, domain in domains.items():
            problem.addVariable(var, domain)
        for constraint in constraints:
            problem.addConstraint(*constraint)
        for var, c_list in vconstraints.items():
            for constraint in c_list:
                problem.addConstraint(*constraint, (var,))
        return problem.getSolution()

    def getSolutions(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        from constraint import Problem
        problem = Problem()
        for var, domain in domains.items():
            problem.addVariable(var, domain)
        for constraint in constraints:
            problem.addConstraint(*constraint)
        for var, c_list in vconstraints.items():
            for constraint in c_list:
                problem.addConstraint(*constraint, (var,))
        return problem.getSolutions()

    def getSolutionIter(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        from constraint import Problem
        problem = Problem()
        for var, domain in domains.items():
            problem.addVariable(var, domain)
        for constraint in constraints:
            problem.addConstraint(*constraint)
        for var, c_list in vconstraints.items():
            for constraint in c_list:
                problem.addConstraint(*constraint, (var,))
        return problem.getSolutionIter()

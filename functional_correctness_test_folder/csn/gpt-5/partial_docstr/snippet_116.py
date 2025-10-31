class Solver:

    def getSolution(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        for sol in self.getSolutionIter(domains, constraints, vconstraints):
            return sol
        return None

    def getSolutions(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        return list(self.getSolutionIter(domains, constraints, vconstraints))

    def getSolutionIter(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        vars_list = list(domains.keys())
        doms = {v: list(domains[v]) for v in vars_list}

        def is_consistent(var, value, assignment):
            related = vconstraints.get(var, [])
            for constraint, cvars in related:
                vals = []
                all_assigned = True
                for cv in cvars:
                    if cv == var:
                        vals.append(value)
                    elif cv in assignment:
                        vals.append(assignment[cv])
                    else:
                        all_assigned = False
                        break
                if all_assigned:
                    try:
                        ok = constraint(*vals)
                    except TypeError:
                        ok = constraint(vals)
                    if not ok:
                        return False
            return True

        def select_unassigned_variable(assignment):
            unassigned = [v for v in vars_list if v not in assignment]
            # MRV heuristic
            return min(unassigned, key=lambda v: len(doms[v]))

        def backtrack(assignment):
            if len(assignment) == len(vars_list):
                yield dict(assignment)
                return
            var = select_unassigned_variable(assignment)
            for value in doms[var]:
                if is_consistent(var, value, assignment):
                    assignment[var] = value
                    yield from backtrack(assignment)
                    del assignment[var]

        return backtrack({})

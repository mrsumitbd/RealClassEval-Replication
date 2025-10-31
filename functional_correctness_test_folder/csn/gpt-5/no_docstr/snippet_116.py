class Solver:
    def _normalize_constraints(self, domains: dict, constraints: list[tuple]):
        norm = []
        for c in constraints:
            # Accept formats:
            # - {'vars': [...], 'func': callable}
            # - (vars, func)
            # - (func, vars)
            if isinstance(c, dict):
                vars_ = c.get('vars')
                func = c.get('func')
            elif isinstance(c, tuple) and len(c) == 2:
                a, b = c
                if callable(a) and (isinstance(b, (list, tuple)) or b is None):
                    func, vars_ = a, b
                elif callable(b) and (isinstance(a, (list, tuple)) or a is None):
                    vars_, func = a, b
                else:
                    raise ValueError(
                        "Constraint tuple must be (vars, func) or (func, vars).")
            else:
                raise ValueError("Unsupported constraint format.")
            if vars_ is None:
                # Global constraint: will be evaluated when all variables are assigned
                vars_ = tuple(domains.keys())
            if not callable(func):
                raise ValueError("Constraint func must be callable.")
            vars_ = tuple(vars_)
            # Validate variables exist
            for v in vars_:
                if v not in domains:
                    raise KeyError(
                        f"Constraint references unknown variable: {v}")
            norm.append((vars_, func))
        return norm

    def _build_vconstraints(self, variables, constraints):
        vmap = {v: [] for v in variables}
        for idx, (vars_, _) in enumerate(constraints):
            for v in vars_:
                vmap[v].append(idx)
        return vmap

    def _is_consistent(self, assignment, constraint, scope):
        # Only evaluate when all vars in scope are assigned
        if any(v not in assignment for v in scope):
            return True
        func_args = [assignment[v] for v in scope]
        return bool(constraint(*func_args))

    def _backtrack(self, vars_order, domains, constraints, vconstraints, assignment):
        if len(assignment) == len(vars_order):
            yield dict(assignment)
            return

        # Choose next unassigned variable (simple order)
        for var in vars_order:
            if var not in assignment:
                next_var = var
                break

        for value in domains[next_var]:
            assignment[next_var] = value
            ok = True
            # Check only constraints that involve next_var; evaluate those whose scope fully assigned
            for cidx in vconstraints.get(next_var, []):
                scope, func = constraints[cidx]
                if not self._is_consistent(assignment, func, scope):
                    ok = False
                    break
            if ok:
                yield from self._backtrack(vars_order, domains, constraints, vconstraints, assignment)
            del assignment[next_var]

    def getSolution(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        solutions = self.getSolutionIter(domains, constraints, vconstraints)
        try:
            return next(solutions)
        except StopIteration:
            return None

    def getSolutions(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        return list(self.getSolutionIter(domains, constraints, vconstraints))

    def getSolutionIter(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        if not isinstance(domains, dict) or not domains:
            return iter(())  # empty iterator

        # Normalize domains to lists
        doms = {v: list(vals) for v, vals in domains.items()}
        norm_constraints = self._normalize_constraints(doms, constraints or [])

        if not vconstraints:
            vmap = self._build_vconstraints(doms.keys(), norm_constraints)
        else:
            # Ensure indices are valid
            vmap = {k: list(vconstraints.get(k, [])) for k in doms.keys()}
        vars_order = list(doms.keys())

        def generator():
            yield from self._backtrack(vars_order, doms, norm_constraints, vmap, {})

        return generator()

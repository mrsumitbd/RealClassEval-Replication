class Hamiltonian:

    def __init__(self, hamiltonian):
        self._hamiltonian = hamiltonian
        self.terms = Terms(self._hamiltonian.terms.children())

    def set_parameter(self, name=None, value=None, scale_factor=None, hamiltonian_name=None):
        if name is None or value is None:
            return
        if name in ['Fk', 'Gk', 'Zeta']:
            parameter = getattr(self._hamiltonian, name.lower(), None)
            if parameter is not None:
                parameter.value = value
                parameter.updateIndividualScaleFactors(value)
        if name == 'Number of Configurations':
            self._hamiltonian.numberOfConfigurations.value = value
        if name == 'Number of States':
            self._hamiltonian.numberOfStates.value = value
        parameters = list(self._hamiltonian.findChild(name))
        for parameter in parameters:
            hamiltonian = parameter.parent()
            if hamiltonian_name is None:
                pass
            elif hamiltonian_name not in hamiltonian.name:
                continue
            if parameter.name == name:
                if value is not None:
                    parameter.value = value
                if scale_factor is not None:
                    parameter.scaleFactor = scale_factor

    def __str__(self):
        data = Tree()
        general_data = Tree()
        general_data['Fk'] = self._hamiltonian.fk.value
        general_data['Gk'] = self._hamiltonian.gk.value
        general_data['Zeta'] = self._hamiltonian.zeta.value
        general_data['Number of States'] = self._hamiltonian.numberOfStates.value
        general_data['Number of Configurations'] = self._hamiltonian.numberOfConfigurations.value
        data['General'] = general_data
        for term in self._hamiltonian.terms.children():
            for hamiltonian in term.children():
                for parameter in hamiltonian.children():
                    parameter_data = [parameter.value]
                    scale_factor = getattr(parameter, 'scaleFactor', None)
                    if scale_factor is not None:
                        parameter_data.append(scale_factor)
                    data['Terms'][term.name][hamiltonian.name][parameter.name] = parameter_data
        return prettify(data)

    def _repr_pretty_(self, p, cycle):
        p.text(str(self) if not cycle else '...')
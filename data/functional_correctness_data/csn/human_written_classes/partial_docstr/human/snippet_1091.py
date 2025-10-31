from ase.thermochemistry import IdealGasThermo
import ase
import numpy as np

class GasMolecule:

    def __init__(self, molecule_name='O2'):
        self.molecule_dict = molecule_dict
        self.name = molecule_name
        self.electronic_energy = molecule_dict[self.name]['electronic_energy']
        self.atom_object = ase.build.molecule(self.name)
        self.pressure = StandardConditions['pressure']
        self.geometry = molecule_dict[self.name]['geometry']
        self.symmetrynumber = molecule_dict[self.name]['symmetrynumber']
        self.spin = molecule_dict[self.name]['spin']
        self.vibrations = molecule_dict[self.name]['vibrations']
        self.enthalpy = None
        self.free_energy = None

    def get_free_energy(self, temperature, pressure='Default', electronic_energy='Default', overbinding=True):
        """Returns the internal energy of an adsorbed molecule.

        Parameters
        ----------
        temperature : numeric
           temperature in K
        electronic_energy : numeric
           energy in eV
        pressure : numeric
           pressure in mbar

        Returns
        -------
        internal_energy : numeric
           Internal energy in eV
        """
        if not temperature or not pressure:
            return 0
        else:
            if electronic_energy == 'Default':
                electronic_energy = molecule_dict[self.name]['electronic_energy']
                if overbinding == True:
                    electronic_energy += molecule_dict[self.name]['overbinding']
            else:
                pass
            if pressure == 'Default':
                pressure = molecule_dict[self.name]['pressure']
            else:
                pass
            pressure = pressure * 100
            ideal_gas_object = IdealGasThermo(vib_energies=self.get_vib_energies(), potentialenergy=electronic_energy, atoms=self.atom_object, geometry=molecule_dict[self.name]['geometry'], symmetrynumber=molecule_dict[self.name]['symmetrynumber'], spin=molecule_dict[self.name]['spin'])
            self.free_energy = ideal_gas_object.get_gibbs_energy(temperature=temperature, pressure=pressure, verbose=False)
            return self.free_energy

    def get_enthalpy(self, temperature, electronic_energy='Default', overbinding=True):
        """Returns the internal energy of an adsorbed molecule.

        Parameters
        ----------
        temperature : numeric
        temperature in K
        electronic_energy : numeric
        energy in eV


        Returns
        -------
        internal_energy : numeric
        Internal energy in eV
        """
        if not temperature:
            return (0, 0, 0)
        if electronic_energy == 'Default':
            electronic_energy = molecule_dict[self.name]['electronic_energy']
            if overbinding == True:
                electronic_energy += molecule_dict[self.name]['overbinding']
        else:
            ideal_gas_object = IdealGasThermo(vib_energies=self.get_vib_energies(), potentialenergy=electronic_energy, atoms=self.atom_object, geometry=molecule_dict[self.name]['geometry'], symmetrynumber=molecule_dict[self.name]['symmetrynumber'], spin=molecule_dict[self.name]['spin'])
            self.enthalpy = ideal_gas_object.get_enthalpy(temperature=temperature, verbose=False)
            return self.enthalpy

    def get_vib_energies(self):
        """Returns a list of vibration in energy units eV.

        Returns
        -------
        vibs : list of vibrations in eV
        """
        vibs = self.molecule_dict[self.name]['vibrations']
        return np.array(vibs) * cm2ev
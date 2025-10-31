from ase.thermochemistry import HarmonicThermo
import numpy as np

class Adsorbate:

    def __init__(self, molecule_name='C'):
        self.molecule_dict = mol_Cu211_dict
        self.name = molecule_name
        self.vibrations = self.molecule_dict[self.name]
        self.vib_energies = np.asarray(self.vibrations) * cm2ev

    def get_helmholtz_energy(self, temperature, electronic_energy=0, verbose=False):
        """Returns the Helmholtz energy of an adsorbed molecule.

        Parameters
        ----------
        temperature : numeric
            temperature in K
        electronic_energy : numeric
            energy in eV
        verbose : boolean
            whether to print ASE thermochemistry output

        Returns
        -------
        helmholtz_energy : numeric
            Helmholtz energy in eV
        """
        thermo_object = HarmonicThermo(vib_energies=self.vib_energies, potentialenergy=electronic_energy)
        self.helmholtz_energy = thermo_object.get_helmholtz_energy(temperature=temperature, verbose=verbose)
        return self.helmholtz_energy

    def get_internal_energy(self, temperature, electronic_energy=0, verbose=False):
        """Returns the internal energy of an adsorbed molecule.

        Parameters
        ----------
        temperature : numeric
            temperature in K
        electronic_energy : numeric
            energy in eV
        verbose : boolean
            whether to print ASE thermochemistry output

        Returns
        -------
        internal_energy : numeric
            Internal energy in eV
        """
        thermo_object = HarmonicThermo(vib_energies=self.vib_energies, potentialenergy=electronic_energy)
        self.internal_energy = thermo_object.get_internal_energy(temperature=temperature, verbose=verbose)
        return self.internal_energy
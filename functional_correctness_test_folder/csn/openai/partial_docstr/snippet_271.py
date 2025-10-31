
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch


class Subplot:
    def __init__(self, ax, energies, number_of_interactions=4, title='', title_font_size=16,
                 state_names=None, virtual=[None], state_font_size=14,
                 state_text_buffer=0.5, label_side='left'):
        """
        Subplot.
        Parameters
        ----------
        ax : matplotlib axis
            The axis.
        energies : 1D array-like
            Energies (scaled between 0 and 1)
        number_of_interactions : integer
            Number of interactions in diagram.
        title : string (optional)
            Title of subplot. Default is empty string.
        state_names: list of str (optional)
            list of the names of the states
        virtual: list of ints (optional)
            list of indexes of any virtual energy states
        state_font_size: numtype (optional)
            font size for the state lables
        state_text_buffer: numtype (optional)
            space between the energy level bars and the state labels
        """
        self.ax = ax
        self.energies = np.asarray(energies)
        self.n_int = number_of_interactions
        self.title = title
        self.title_font_size = title_font_size
        self.state_names = state_names if state_names is not None else [
            f'S{i}' for i in range(len(energies))]
        self.virtual = set(v for v in virtual


import matplotlib.pyplot as plt
import numpy as np


class Subplot:
    '''Subplot containing WMEL.'''

    def __init__(self, ax, energies, number_of_interactions=4, title='', title_font_size=16,
                 state_names=None, virtual=[None], state_font_size=14,
                 state_text_buffer=0.5, label_side='left'):
        '''Subplot.
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
        '''
        self.ax = ax
        self.energies = np.asarray(energies)
        self.n_int = number_of_interactions
        self.title = title
        self.title_font_size = title_font_size
        self.state_names = state_names if state_names is not None else [
            f'S{i}' for i in range(len(energies))]
        self.virtual = set(v for v in virtual if v is not None)
        self.state_font_size = state_font_size
        self.state_text_buffer = state_text_buffer
        self.label_side = label_side

        # Draw horizontal energy level lines
        for i, y in enumerate(self.energies):
            if i in self.virtual:
                continue
            self.ax.hlines(y, 0, self.n_int - 1, color='k', linewidth=2)

        # Label states
        for i, y in enumerate(self.energies):
            if i in self.virtual:
                continue
            if self.label_side == 'left':
                x = -self.state_text_buffer
                ha = 'right'
            else:
                x = self.n_int - 1 + self.state_text_buffer
                ha = 'left'
            self.ax.text(x, y, self.state_names[i], fontsize=self.state_font_size,
                         ha=ha, va='center')

        # Set limits and title
        self.ax.set_xlim(-self.state_text_buffer,
                         self.n_int - 1 + self.state_text_buffer)
        self.ax.set_ylim(0, 1)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        if self.title:
            self.ax.set_title(self.title, fontsize=self.title_font_size)

    def add_arrow(self, index, between, kind, label='', head_length=10,
                  head_aspect=1, font_size=14, color='k'):
        '''Add an arrow to the WMEL diagram.
        Parameters
        ----------
        index : integer
            The interaction, or start and stop interaction for the arrow.
        between : 2-element iterable of integers
            The inital and final state of the arrow
        kind : {'ket', 'bra', 'outbra', 'outket'}
            The kind of interaction.
        label : string (optional)
            Interaction label. Default is empty string.
        head_length: number (optional)
            size of arrow head
        font_size : number (optional)
            Label font size. Default is 14.
        color : matplotlib color (optional)
            Arrow color. Default is black.
        Returns
        -------
        [annotation, text]
        '''
        start, end = between
        y_start = self.energies[start]
        y_end = self.energies[end]
        x = index

        # Determine arrow direction and positions
        if kind == 'ket':
            xytext = (x, y_start)
            xy = (x, y_end)
            midx, midy = x, (y_start + y_end) / 2
        elif kind == 'bra':
            xytext = (x, y_end)
            xy = (x, y_start)
            midx, midy = x, (y_start + y_end) / 2
        elif kind == 'outbra':
            xytext = (x - 0.5, y_start)
            xy = (x, y_start)
            midx, midy = x - 0.25, y_start
        elif kind == 'outket':
            xytext = (x + 0.5, y_end)
            xy = (x, y_end)
            midx, midy = x + 0.25, y_end
        else:
            raise ValueError(
                f"Unknown kind '{kind}'. Must be one of 'ket', 'bra', 'outbra', 'outket'.")

        # Draw arrow
        arrow = self.ax.annotate('',
                                 xy=xy, xytext=xytext,

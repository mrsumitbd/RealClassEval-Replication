
import matplotlib.pyplot as plt
import numpy as np


class Subplot:
    '''Subplot containing WMEL.'''

    def __init__(self, ax, energies, number_of_interactions=4, title='', title_font_size=16, state_names=None, virtual=[None], state_font_size=14, state_text_buffer=0.5, label_side='left'):
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
            list of indexes of any vitual energy states
        state_font_size: numtype (optional)
            font size for the state lables
        state_text_buffer: numtype (optional)
            space between the energy level bars and the state labels
        '''
        self.ax = ax
        self.energies = energies
        self.number_of_interactions = number_of_interactions
        self.title = title
        self.title_font_size = title_font_size
        self.state_names = state_names
        self.virtual = virtual
        self.state_font_size = state_font_size
        self.state_text_buffer = state_text_buffer
        self.label_side = label_side

        self._draw()

    def _draw(self):
        self.ax.set_xlim(0, self.number_of_interactions)
        self.ax.set_ylim(0, 1)
        self.ax.set_title(self.title, fontsize=self.title_font_size)

        for i, energy in enumerate(self.energies):
            if i in self.virtual:
                self.ax.plot([0, self.number_of_interactions], [
                             energy, energy], 'k--', linewidth=2)
            else:
                self.ax.plot([0, self.number_of_interactions], [
                             energy, energy], 'k-', linewidth=2)

            if self.state_names is not None:
                if self.label_side == 'left':
                    self.ax.text(-self.state_text_buffer, energy,
                                 self.state_names[i], fontsize=self.state_font_size, ha='right', va='center')
                else:
                    self.ax.text(self.number_of_interactions + self.state_text_buffer, energy,
                                 self.state_names[i], fontsize=self.state_font_size, ha='left', va='center')

        self.ax.set_xticks(np.arange(self.number_of_interactions + 1))
        self.ax.set_yticks([])

    def add_arrow(self, index, between, kind, label='', head_length=10, head_aspect=1, font_size=14, color='k'):
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
        [line,arrow_head,text]
        '''
        if kind == 'ket':
            x = [index, index]
            y = [self.energies[between[0]], self.energies[between[1]]]
            arrow_head = self.ax.arrow(x[0], y[0], 0, y[1] - y[0], head_width=0.05,
                                       head_length=head_length, fc=color, ec=color, head_starts_at_zero=False)
        elif kind == 'bra':
            x = [index, index]
            y = [self.energies[between[1]], self.energies[between[0]]]
            arrow_head = self.ax.arrow(x[0], y[0], 0, y[1] - y[0], head_width=0.05,
                                       head_length=head_length, fc=color, ec=color, head_starts_at_zero=False)
        elif kind == 'outbra':
            x = [index[0], index[1]]
            y = [self.energies[between[1]], self.energies[between[0]]]
            arrow_head = self.ax.arrow(x[0], y[0], x[1] - x[0], y[1] - y[0], head_width=0.05,
                                       head_length=head_length, fc=color, ec=color, head_starts_at_zero=False)
        elif kind == 'outket':
            x = [index[0], index[1]]
            y = [self.energies[between[0]], self.energies[between[1]]]
            arrow_head = self.ax.arrow(x[0], y[0], x[1] - x[0], y[1] - y[0], head_width=0.05,
                                       head_length=head_length, fc=color, ec=color, head_starts_at_zero=False)

        line = self.ax.plot(x, y, color=color, linewidth=2)
        text = self.ax.text(np.mean(x), np.mean(y), label,
                            fontsize=font_size, ha='center', va='center')

        return [line, arrow_head, text]

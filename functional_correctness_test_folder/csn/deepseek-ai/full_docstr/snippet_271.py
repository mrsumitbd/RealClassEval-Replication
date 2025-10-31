
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
        self.energies = np.asarray(energies)
        self.number_of_interactions = number_of_interactions
        self.title = title
        self.state_names = state_names if state_names is not None else [
            f'|{i}⟩' for i in range(len(energies))]
        self.virtual = virtual
        self.state_font_size = state_font_size
        self.state_text_buffer = state_text_buffer
        self.label_side = label_side

        self._setup_plot()

    def _setup_plot(self):
        self.ax.set_title(self.title, fontsize=self.title_font_size)
        self.ax.set_xlim(0, self.number_of_interactions + 1)
        self.ax.set_ylim(0, 1.1)
        self.ax.set_xticks(range(1, self.number_of_interactions + 1))
        self.ax.set_xticklabels(range(1, self.number_of_interactions + 1))
        self.ax.set_yticks([])

        for i, energy in enumerate(self.energies):
            linestyle = '--' if i in self.virtual else '-'
            self.ax.hlines(energy, 1, self.number_of_interactions,
                           colors='k', linestyles=linestyle)

            if self.label_side == 'left':
                self.ax.text(1 - self.state_text_buffer, energy, self.state_names[i],
                             ha='right', va='center', fontsize=self.state_font_size)
            else:
                self.ax.text(self.number_of_interactions + self.state_text_buffer, energy, self.state_names[i],
                             ha='left', va='center', fontsize=self.state_font_size)

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
        start_state, end_state = between
        x = index if isinstance(index, (int, float)) else np.linspace(
            index[0], index[1], 100)
        y_start = self.energies[start_state]
        y_end = self.energies[end_state]

        if kind == 'ket':
            arrow_direction = 1
        elif kind == 'bra':
            arrow_direction = -1
        elif kind == 'outket':
            arrow_direction = 1
        elif kind == 'outbra':
            arrow_direction = -1
        else:
            raise ValueError(
                "Invalid kind. Must be 'ket', 'bra', 'outket', or 'outbra'.")

        if isinstance(index, (int, float)):
            line = self.ax.vlines(x, y_start, y_end, colors=color)
            arrow_head = self.ax.arrow(x, y_end, 0, arrow_direction * 0.01, head_width=head_length/100,
                                       head_length=head_length/100 * head_aspect, fc=color, ec=color)
        else:
            line, = self.ax.plot(x, np.linspace(
                y_start, y_end, 100), color=color)
            arrow_head = self.ax.arrow(x[-1], y_end, 0, arrow_direction * 0.01, head_width=head_length/100,
                                       head_length=head_length/100 * head_aspect, fc=color, ec=color)

        if label:
            text = self.ax.text(x if isinstance(index, (int, float)) else np.mean(x),
                                (y_start + y_end) / 2, label, ha='center', va='center',
                                fontsize=font_size, color=color)
        else:
            text = None

        return [line, arrow_head, text]

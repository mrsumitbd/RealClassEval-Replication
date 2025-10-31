
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
        self.energies = np.array(energies)
        self.n_states = len(self.energies)
        self.n_interactions = number_of_interactions
        self.title = title
        self.title_font_size = title_font_size
        self.state_names = state_names if state_names is not None else [
            f'State {i}' for i in range(self.n_states)]
        self.virtual = virtual if virtual is not None else [None]
        self.state_font_size = state_font_size
        self.state_text_buffer = state_text_buffer
        self.label_side = label_side

        # Set up the subplot
        self._draw_energy_levels()
        if self.title:
            self.ax.set_title(self.title, fontsize=self.title_font_size)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xlim(-0.5, self.n_interactions - 0.5)
        self.ax.set_ylim(-0.1, 1.1)

    def _draw_energy_levels(self):
        # Draw horizontal lines for each energy level at each interaction
        for i, energy in enumerate(self.energies):
            color = 'gray' if (
                self.virtual is not None and i in self.virtual) else 'k'
            for x in range(self.n_interactions):
                self.ax.hlines(energy, x-0.3, x+0.3,
                               color=color, linewidth=2, zorder=1)
            # Draw state label
            if self.label_side == 'left':
                x_text = -0.5 - self.state_text_buffer
                ha = 'right'
            else:
                x_text = self.n_interactions - 0.5 + self.state_text_buffer
                ha = 'left'
            self.ax.text(
                x_text, energy, self.state_names[i],
                va='center', ha=ha, fontsize=self.state_font_size,
                color=color, zorder=2
            )

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
        # Determine x positions
        if isinstance(index, (list, tuple, np.ndarray)) and len(index) == 2:
            x0, x1 = index
        else:
            x0 = x1 = index

        y0 = self.energies[between[0]]
        y1 = self.energies[between[1]]

        # For 'ket' and 'bra', arrow is vertical at a single interaction
        # For 'outket' and 'outbra', arrow is horizontal between two interactions
        if kind in ('ket', 'bra'):
            x = x0
            dx = 0
            dy = y1 - y0
            start = (x, y0)
            end = (x, y1)
            if kind == 'ket':
                arrow_dir = 1
            else:
                arrow_dir = -1
            # Draw line
            line = self.ax.plot(
                [x, x], [y0, y1], color=color, linewidth=2, zorder=3)[0]
            # Draw arrow head
            arrow_head = self.ax.arrow(
                x, y1 if arrow_dir > 0 else y0,
                0, 0.001*arrow_dir,  # tiny length, just to show head
                head_width=0.1, head_length=0.03*head_length, fc=color, ec=color,
                length_includes_head=True, overhang=0.3, zorder=4
            )
            # Label
            if label:
                y_label = (y0 + y1) / 2
                x_label = x + 0.15
                text = self.ax.text(
                    x_label, y_label, label, fontsize=font_size,
                    va='center', ha='left', color=color, zorder=5
                )
            else:
                text = None
        elif kind in ('outket', 'outbra'):
            y = y0
            dx = x1 - x0
            dy = 0
            start = (x0, y)
            end = (x1, y)
            if kind == 'outket':
                arrow_dir = 1
            else:
                arrow_dir = -1
            # Draw line
            line = self.ax.plot(
                [x0, x1], [y, y], color=color, linewidth=2, zorder=3)[0]
            # Draw arrow head
            arrow_head = self.ax.arrow(
                x1 if arrow_dir > 0 else x0, y,
                0.001*arrow_dir, 0,  # tiny length, just to show head
                head_width=0.03*head_length, head_length=0.1, fc=color, ec=color,
                length_includes_head=True, overhang=0.3, zorder=4
            )
            # Label
            if label:
                x_label = (x0 + x1) / 2
                y_label = y + 0.05
                text = self.ax.text(
                    x_label, y_label, label, fontsize=font_size,
                    va='bottom', ha='center', color=color, zorder=5
                )
            else:
                text = None
        else:
            raise ValueError(
                "kind must be one of {'ket', 'bra', 'outbra', 'outket'}")

        return [line, arrow_head, text]

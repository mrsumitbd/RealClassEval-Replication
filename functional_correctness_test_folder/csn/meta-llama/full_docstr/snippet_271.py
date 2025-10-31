
import matplotlib.pyplot as plt
import matplotlib.patches as patches
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
        self.number_of_interactions = number_of_interactions
        self.title = title
        self.title_font_size = title_font_size
        self.state_names = state_names if state_names is not None else [
            f'State {i}' for i in range(len(energies))]
        self.virtual = virtual
        self.state_font_size = state_font_size
        self.state_text_buffer = state_text_buffer
        self.label_side = label_side

        self.ax.set_xlim(-1, number_of_interactions + 1)
        self.ax.set_ylim(min(energies) - 0.1, max(energies) + 0.1)
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        for i, energy in enumerate(energies):
            self.ax.plot([-1, number_of_interactions],
                         [energy, energy], 'k--', alpha=0.5)
            if label_side == 'left':
                self.ax.text(-1 - state_text_buffer, energy,
                             self.state_names[i], ha='right', va='center', fontsize=state_font_size)
            elif label_side == 'right':
                self.ax.text(number_of_interactions + state_text_buffer, energy,
                             self.state_names[i], ha='left', va='center', fontsize=state_font_size)

        self.ax.set_title(title, fontsize=title_font_size)

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
        if kind not in ['ket', 'bra', 'outbra', 'outket']:
            raise ValueError(
                "Invalid kind. Must be 'ket', 'bra', 'outbra', or 'outket'.")

        initial_energy = self.energies[between[0]]
        final_energy = self.energies[between[1]]

        if isinstance(index, int):
            x = index
            dx = 0
        else:
            x = index[0]
            dx = index[1] - index[0]

        line = self.ax.plot([x, x + dx], [initial_energy,
                            final_energy], color=color)[0]

        if kind in ['ket', 'outket']:
            arrow_head = patches.FancyArrowPatch((x + dx, final_energy), (x + 0.9*dx, final_energy - (final_energy - initial_energy)*0.9),
                                                 arrowstyle=patches.ArrowStyle(
                                                     'Simple', head_length=head_length, head_width=head_length*head_aspect),
                                                 color=color, mutation_scale=10)
        else:
            arrow_head = patches.FancyArrowPatch((x + dx, final_energy), (x + 0.9*dx, final_energy - (final_energy - initial_energy)*0.9),
                                                 arrowstyle=patches.ArrowStyle(
                                                     'Simple', head_length=head_length, head_width=head_length*head_aspect),
                                                 color=color, mutation_scale=10)
            arrow_head.set_arrowstyle(patches.ArrowStyle(
                'Simple', head_length=head_length, head_width=head_length*head_aspect))

        self.ax.add_patch(arrow_head)

        text = self.ax.text(x + dx/2, (initial_energy + final_energy)/2,
                            label, ha='center', va='center', fontsize=font_size)

        return [line, arrow_head, text]

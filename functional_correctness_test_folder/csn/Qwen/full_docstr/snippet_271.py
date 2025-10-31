
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
        self.energies = energies
        self.number_of_interactions = number_of_interactions
        self.title = title
        self.title_font_size = title_font_size
        self.state_names = state_names if state_names else [
            f'State {i}' for i in range(len(energies))]
        self.virtual = virtual
        self.state_font_size = state_font_size
        self.state_text_buffer = state_text_buffer
        self.label_side = label_side

        self.ax.set_title(self.title, fontsize=self.title_font_size)
        self.ax.set_xlim(0, self.number_of_interactions)
        self.ax.set_ylim(-0.1, 1.1)
        self.ax.set_yticks(self.energies)
        self.ax.set_yticklabels(
            self.state_names, fontsize=self.state_font_size)
        self.ax.set_xticks(range(self.number_of_interactions + 1))
        self.ax.set_xticklabels([])

        for i, energy in enumerate(self.energies):
            if i in self.virtual:
                self.ax.axhline(y=energy, color='gray', linestyle='--')
            else:
                self.ax.axhline(y=energy, color='black', linestyle='-')

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
        start_energy = self.energies[start_state]
        end_energy = self.energies[end_state]

        if kind == 'ket':
            arrow = patches.FancyArrowPatch((index, start_energy), (index + 1, end_energy),
                                            arrowstyle=f'-|>,head_length={head_length},head_width={head_length / head_aspect}',
                                            mutation_scale=10, color=color)
        elif kind == 'bra':
            arrow = patches.FancyArrowPatch((index + 1, end_energy), (index, start_energy),
                                            arrowstyle=f'-|>,head_length={head_length},head_width={head_length / head_aspect}',
                                            mutation_scale=10, color=color)
        elif kind == 'outbra':
            arrow = patches.FancyArrowPatch((index, end_energy), (index + 1, start_energy),
                                            arrowstyle=f'-|>,head_length={head_length},head_width={head_length / head_aspect}',
                                            mutation_scale=10, color=color)
        elif kind == 'outket':
            arrow = patches.FancyArrowPatch((index + 1, start_energy), (index, end_energy),
                                            arrowstyle=f'-|>,head_length={head_length},head_width={head_length / head_aspect}',
                                            mutation_scale=10, color=color)
        else:
            raise ValueError(
                "kind must be one of 'ket', 'bra', 'outbra', 'outket'")

        self.ax.add_patch(arrow)

        if self.label_side == 'left':
            text_x = index - 0.1
        else:
            text_x = index + 1.1

        text_y = (start_energy + end_energy) / 2
        text = self.ax.text(text_x, text_y, label, fontsize=font_size,
                            color=color, ha='center', va='center')

        return [arrow, arrow, text]

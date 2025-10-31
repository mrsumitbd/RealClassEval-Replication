
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


class Subplot:

    def __init__(self, ax, energies, number_of_interactions=4, title='', title_font_size=16, state_names=None, virtual=[None], state_font_size=14, state_text_buffer=0.5, label_side='left'):
        self.ax = ax
        self.energies = energies
        self.number_of_interactions = number_of_interactions
        self.title = title
        self.title_font_size = title_font_size
        self.state_names = state_names if state_names is not None else [
            f'State {i}' for i in range(len(energies))]
        self.virtual = virtual
        self.state_font_size = state_font_size
        self.state_text_buffer = state_text_buffer
        self.label_side = label_side

        self.ax.set_title(self.title, fontsize=self.title_font_size)
        self.ax.set_ylim(-0.1, 1.1)
        self.ax.set_xlim(-0.1, self.number_of_interactions + 0.1)
        self.ax.set_yticks(self.energies)
        self.ax.set_yticklabels(
            self.state_names, fontsize=self.state_font_size)
        self.ax.set_xticks(range(self.number_of_interactions))
        self.ax.set_xticklabels([])
        self.ax.set_xlabel('Interactions')
        self.ax.grid(True, which='both', axis='y',
                     linestyle='--', linewidth=0.5)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.yaxis.set_ticks_position('left')
        self.ax.xaxis.set_ticks_position('bottom')

        for i, energy in enumerate(self.energies):
            self.ax.plot([0, self.number_of_interactions], [
                         energy, energy], 'k-', linewidth=1.5)
            if i in self.virtual:
                self.ax.plot([0, self.number_of_interactions], [
                             energy, energy], 'k--', linewidth=1.5)
            if self.label_side == 'left':
                self.ax.text(-self.state_text_buffer, energy,
                             self.state_names[i], fontsize=self.state_font_size, ha='right', va='center')
            else:
                self.ax.text(self.number_of_interactions + self.state_text_buffer, energy,
                             self.state_names[i], fontsize=self.state_font_size, ha='left', va='center')

    def add_arrow(self, index, between, kind, label='', head_length=10, head_aspect=1, font_size=14, color='k'):
        start_state, end_state = between
        start_energy = self.energies[start_state]
        end_energy = self.energies[end_state]
        x_start = index
        x_end = index + 1 if kind in ['ket', 'outket'] else index - \
            1 if kind in ['bra', 'outbra'] else index

        arrow = patches.FancyArrowPatch((x_start, start_energy), (x_end, end_energy),
                                        arrowstyle=f'-|>,head_length={head_length},head_width={head_length / head_aspect}', mutation_scale=10, color=color)
        self.ax.add_patch(arrow)

        if kind in ['ket', 'bra']:
            text_x = (x_start + x_end) / 2
            text_y = (start_energy + end_energy) / 2
        elif kind in ['outket', 'outbra']:
            text_x = (x_start + x_end) / 2
            text_y = (start_energy + end_energy) / 2 + \
                0.05 if kind == 'outket' else (
                    start_energy + end_energy) / 2 - 0.05

        text = self.ax.text(text_x, text_y, label, fontsize=font_size,
                            ha='center', va='center', color=color)

        return [arrow, text]

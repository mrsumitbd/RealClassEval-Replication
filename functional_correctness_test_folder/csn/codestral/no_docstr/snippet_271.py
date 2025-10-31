
import matplotlib.pyplot as plt
import numpy as np


class Subplot:

    def __init__(self, ax, energies, number_of_interactions=4, title='', title_font_size=16, state_names=None, virtual=[None], state_font_size=14, state_text_buffer=0.5, label_side='left'):

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

        self.ax.set_title(self.title, fontsize=self.title_font_size)
        self.ax.set_yticks(self.energies)
        self.ax.set_yticklabels(
            self.state_names, fontsize=self.state_font_size)
        self.ax.set_xticks([])

        for i, energy in enumerate(self.energies):
            if i in self.virtual:
                self.ax.axhline(y=energy, color='k', linestyle='--')
            else:
                self.ax.axhline(y=energy, color='k')

            if self.label_side == 'left':
                self.ax.text(-self.state_text_buffer, energy,
                             self.state_names[i], fontsize=self.state_font_size, ha='right', va='center')
            else:
                self.ax.text(self.number_of_interactions + self.state_text_buffer, energy,
                             self.state_names[i], fontsize=self.state_font_size, ha='left', va='center')

    def add_arrow(self, index, between, kind, label='', head_length=10, head_aspect=1, font_size=14, color='k'):

        start_energy = self.energies[between[0]]
        end_energy = self.energies[between[1]]
        x_start = index
        x_end = index

        if kind == 'up':
            y_start = start_energy
            y_end = end_energy
        elif kind == 'down':
            y_start = end_energy
            y_end = start_energy
        else:
            raise ValueError("kind must be either 'up' or 'down'")

        self.ax.annotate('', xy=(x_end, y_end), xytext=(x_start, y_start),
                         arrowprops=dict(arrowstyle='->', color=color, head_length=head_length, head_width=head_length/head_aspect))

        if label:
            x_mid = (x_start + x_end) / 2
            y_mid = (y_start + y_end) / 2
            self.ax.text(x_mid, y_mid, label, fontsize=font_size,
                         ha='center', va='center')

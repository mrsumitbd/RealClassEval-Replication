
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

        self._draw()

    def _draw(self):
        self.ax.set_ylim(0, 1)
        self.ax.set_xlim(0, self.number_of_interactions)
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

        self.ax.set_xticks(np.arange(0, self.number_of_interactions + 1, 1))
        self.ax.set_yticks([])

    def add_arrow(self, index, between, kind, label='', head_length=10, head_aspect=1, font_size=14, color='k'):
        start, end = between
        y_start = self.energies[start]
        y_end = self.energies[end]

        if kind == 'ket':
            x_start = index
            x_end = index
            arrowprops = dict(arrowstyle='->', color=color,
                              head_length=head_length, head_width=head_length/head_aspect)
        elif kind == 'bra':
            x_start = index + 1
            x_end = index + 1
            arrowprops = dict(arrowstyle='<-', color=color,
                              head_length=head_length, head_width=head_length/head_aspect)
        elif kind == 'outbra':
            x_start = index[0] + 1
            x_end = index[1] + 1
            arrowprops = dict(arrowstyle='<-', color=color,
                              head_length=head_length, head_width=head_length/head_aspect)
        elif kind == 'outket':
            x_start = index[0]
            x_end = index[1]
            arrowprops = dict(arrowstyle='->', color=color,
                              head_length=head_length, head_width=head_length/head_aspect)

        line = self.ax.annotate('', xy=(x_end, y_end), xytext=(
            x_start, y_start), arrowprops=arrowprops)
        arrow_head = line.arrow_patch
        text = self.ax.text((x_start + x_end) / 2, (y_start + y_end) / 2,
                            label, fontsize=font_size, ha='center', va='center')

        return [line, arrow_head, text]

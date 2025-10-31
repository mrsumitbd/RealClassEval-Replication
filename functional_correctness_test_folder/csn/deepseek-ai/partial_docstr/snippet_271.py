
import matplotlib.pyplot as plt
import numpy as np


class Subplot:

    def __init__(self, ax, energies, number_of_interactions=4, title='', title_font_size=16, state_names=None, virtual=[None], state_font_size=14, state_text_buffer=0.5, label_side='left'):
        self.ax = ax
        self.energies = np.array(energies)
        self.number_of_interactions = number_of_interactions
        self.title = title
        self.state_names = state_names
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
        self.ax.grid(axis='x', linestyle='--', alpha=0.7)

        for i, energy in enumerate(self.energies):
            color = 'r' if i in self.virtual else 'k'
            self.ax.hlines(
                energy, 1, self.number_of_interactions, colors=color, lw=2)

            if self.state_names is not None and i < len(self.state_names):
                if self.label_side == 'left':
                    self.ax.text(1 - self.state_text_buffer, energy, self.state_names[i],
                                 ha='right', va='center', fontsize=self.state_font_size)
                else:
                    self.ax.text(self.number_of_interactions + self.state_text_buffer, energy, self.state_names[i],
                                 ha='left', va='center', fontsize=self.state_font_size)

    def add_arrow(self, index, between, kind, label='', head_length=10, head_aspect=1, font_size=14, color='k'):
        if isinstance(index, int):
            x_start = x_end = index
        else:
            x_start, x_end = index

        y_start = self.energies[between[0]]
        y_end = self.energies[between[1]]

        line = self.ax.plot([x_start, x_end], [
                            y_start, y_end], color=color, lw=2)[0]

        dx = x_end - x_start
        dy = y_end - y_start

        if kind == 'ket':
            head_angle = np.arctan2(dy, dx) * 180 / np.pi
            arrow_head = self.ax.arrow(x_end, y_end, 0.01 * dx, 0.01 * dy,
                                       head_width=head_length * head_aspect,
                                       head_length=head_length,
                                       fc=color, ec=color, shape='left',
                                       length_includes_head=True)
        elif kind == 'bra':
            head_angle = np.arctan2(-dy, -dx) * 180 / np.pi
            arrow_head = self.ax.arrow(x_start, y_start, -0.01 * dx, -0.01 * dy,
                                       head_width=head_length * head_aspect,
                                       head_length=head_length,
                                       fc=color, ec=color, shape='left',
                                       length_includes_head=True)
        elif kind == 'outket':
            head_angle = np.arctan2(dy, dx) * 180 / np.pi
            arrow_head = self.ax.arrow(x_end, y_end, 0.01 * dx, 0.01 * dy,
                                       head_width=head_length * head_aspect,
                                       head_length=head_length,
                                       fc=color, ec=color, shape='right',
                                       length_includes_head=True)
        elif kind == 'outbra':
            head_angle = np.arctan2(-dy, -dx) * 180 / np.pi
            arrow_head = self.ax.arrow(x_start, y_start, -0.01 * dx, -0.01 * dy,
                                       head_width=head_length * head_aspect,
                                       head_length=head_length,
                                       fc=color, ec=color, shape='right',
                                       length_includes_head=True)
        else:
            raise ValueError(
                "Invalid kind. Must be 'ket', 'bra', 'outket', or 'outbra'.")

        if label:
            x_mid = (x_start + x_end) / 2
            y_mid = (y_start + y_end) / 2
            text = self.ax.text(x_mid, y_mid, label, ha='center', va='center',
                                fontsize=font_size, color=color)
        else:
            text = None

        return [line, arrow_head, text] if text else [line, arrow_head]

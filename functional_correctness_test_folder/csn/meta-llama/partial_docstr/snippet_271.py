
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


class Subplot:

    def __init__(self, ax, energies, number_of_interactions=4, title='', title_font_size=16, state_names=None, virtual=[None], state_font_size=14, state_text_buffer=0.5, label_side='left'):
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

        self.ax.set_xlim(0, number_of_interactions)
        self.ax.set_ylim(-0.1, 1.1)
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        for i, energy in enumerate(self.energies):
            self.ax.plot([0, number_of_interactions], [energy, energy], 'k-')
            if label_side == 'left':
                self.ax.text(-state_text_buffer, energy,
                             self.state_names[i], ha='right', va='center', fontsize=state_font_size)
            else:
                self.ax.text(number_of_interactions + state_text_buffer, energy,
                             self.state_names[i], ha='left', va='center', fontsize=state_font_size)

        self.ax.set_title(title, fontsize=title_font_size)

    def add_arrow(self, index, between, kind, label='', head_length=10, head_aspect=1, font_size=14, color='k'):
        start_state, end_state = between
        start_energy = self.energies[start_state]
        end_energy = self.energies[end_state]

        if kind == 'ket':
            x_start, x_end = index, index + 1
            y_start, y_end = start_energy, end_energy
            arrow_head = patches.FancyArrowPatch(
                (x_end, y_end), (x_start, y_start), arrowstyle=f'->,head_length={head_length},head_width={head_length/head_aspect}', color=color, mutation_scale=10)
        elif kind == 'bra':
            x_start, x_end = index + 1, index
            y_start, y_end = start_energy, end_energy
            arrow_head = patches.FancyArrowPatch(
                (x_end, y_end), (x_start, y_start), arrowstyle=f'->,head_length={head_length},head_width={head_length/head_aspect}', color=color, mutation_scale=10)
        elif kind == 'outket':
            x_start, x_end = index, index + 1
            y_start, y_end = start_energy, end_energy
            arrow_head = patches.FancyArrowPatch((x_start, y_start), (
                x_end, y_end), arrowstyle=f'->,head_length={head_length},head_width={head_length/head_aspect}', color=color, mutation_scale=10)
        elif kind == 'outbra':
            x_start, x_end = index + 1, index
            y_start, y_end = start_energy, end_energy
            arrow_head = patches.FancyArrowPatch((x_start, y_start), (
                x_end, y_end), arrowstyle=f'->,head_length={head_length},head_width={head_length/head_aspect}', color=color, mutation_scale=10)
        else:
            raise ValueError(
                "Invalid kind. Must be 'ket', 'bra', 'outket', or 'outbra'.")

        line = self.ax.plot([x_start + 0.5, x_end - 0.5],
                            [y_start, y_end], color=color, linestyle='--', linewidth=1)
        self.ax.add_patch(arrow_head)
        text = self.ax.text((x_start + x_end) / 2, (y_start + y_end) / 2,
                            label, ha='center', va='center', fontsize=font_size)

        return [line[0], arrow_head, text]


# Example usage:
fig, ax = plt.subplots()
subplot = Subplot(ax, [0.2, 0.5, 0.8],
                  number_of_interactions=4, title='Example WMEL Diagram')
subplot.add_arrow(0, (0, 1), 'ket', label='Interaction 1')
subplot.add_arrow(1, (1, 2), 'bra', label='Interaction 2')
subplot.add_arrow(2, (2, 1), 'outket', label='Interaction 3')
subplot.add_arrow(3, (1, 0), 'outbra', label='Interaction 4')
plt.show()

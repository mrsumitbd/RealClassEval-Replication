
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Subplot:

    def __init__(self, ax, energies, number_of_interactions=4, title='', title_font_size=16, state_names=None, virtual=[None], state_font_size=14, state_text_buffer=0.5, label_side='left'):
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
        self.ax.set_yticks(self.energies)
        self.ax.set_yticklabels(
            self.state_names, fontsize=self.state_font_size)
        self.ax.set_xticks([])

        if self.label_side == 'left':
            self.ax.yaxis.tick_left()
        elif self.label_side == 'right':
            self.ax.yaxis.tick_right()
        else:
            raise ValueError(
                "Invalid label_side. It should be either 'left' or 'right'.")

        for i, energy in enumerate(self.energies):
            if energy in self.virtual:
                self.ax.axhline(y=energy, color='gray', linestyle='--')
            else:
                self.ax.axhline(y=energy, color='k')

    def add_arrow(self, index, between, kind, label='', head_length=10, head_aspect=1, font_size=14, color='k'):
        if kind not in ['up', 'down']:
            raise ValueError(
                "Invalid kind. It should be either 'up' or 'down'.")

        start_energy = self.energies[index]
        end_energy = self.energies[between]

        if kind == 'up' and start_energy > end_energy:
            raise ValueError(
                "Invalid arrow direction. 'up' arrow should have start energy less than end energy.")
        if kind == 'down' and start_energy < end_energy:
            raise ValueError(
                "Invalid arrow direction. 'down' arrow should have start energy greater than end energy.")

        self.ax.arrow(0, start_energy, 0, end_energy - start_energy,
                      head_width=0.1, head_length=head_length,
                      length_includes_head=True, color=color,
                      head_starts_at_zero=False if kind == 'up' else True)

        if label:
            self.ax.text(0.1 if self.label_side == 'left' else -0.1, (start_energy + end_energy) / 2,
                         label, ha='left' if self.label_side == 'left' else 'right',
                         fontsize=font_size)

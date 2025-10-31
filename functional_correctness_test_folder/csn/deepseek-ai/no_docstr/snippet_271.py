
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

        self._setup_plot()

    def _setup_plot(self):
        self.ax.set_title(self.title, fontsize=self.title_font_size)
        self.ax.set_yticks(self.energies)
        self.ax.set_yticklabels(
            self.state_names, fontsize=self.state_font_size)
        self.ax.set_ylim(min(self.energies) - 1, max(self.energies) + 1)
        self.ax.set_xlim(0, self.number_of_interactions + 1)
        self.ax.set_xticks([])
        self.ax.grid(True, axis='y')

        for i, energy in enumerate(self.energies):
            if self.virtual[i] is not None:
                linestyle = '--'
            else:
                linestyle = '-'
            self.ax.hlines(energy, 1, self.number_of_interactions,
                           linestyles=linestyle, colors='k')

    def add_arrow(self, index, between, kind, label='', head_length=10, head_aspect=1, font_size=14, color='k'):
        x_start = between[0]
        x_end = between[1]
        y_start = self.energies[index[0]]
        y_end = self.energies[index[1]]

        if kind == 'absorption':
            dx = x_end - x_start
            dy = y_end - y_start
            self.ax.arrow(x_start, y_start, dx, dy, head_width=head_length, head_length=head_length * head_aspect,
                          fc=color, ec=color, length_includes_head=True)
        elif kind == 'emission':
            dx = x_end - x_start
            dy = y_start - y_end
            self.ax.arrow(x_start, y_start, dx, -dy, head_width=head_length, head_length=head_length * head_aspect,
                          fc=color, ec=color, length_includes_head=True)

        mid_x = (x_start + x_end) / 2
        mid_y = (y_start + y_end) / 2

        if self.label_side == 'left':
            ha = 'right'
            x_text = mid_x - self.state_text_buffer
        else:
            ha = 'left'
            x_text = mid_x + self.state_text_buffer

        self.ax.text(x_text, mid_y, label, ha=ha, va='center',
                     fontsize=font_size, color=color)

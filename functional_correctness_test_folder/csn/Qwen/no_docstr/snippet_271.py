
class Subplot:

    def __init__(self, ax, energies, number_of_interactions=4, title='', title_font_size=16, state_names=None, virtual=[None], state_font_size=14, state_text_buffer=0.5, label_side='left'):
        self.ax = ax
        self.energies = energies
        self.number_of_interactions = number_of_interactions
        self.title = title
        self.title_font_size = title_font_size
        self.state_names = state_names if state_names is not None else [
            f'State {i+1}' for i in range(len(energies))]
        self.virtual = virtual
        self.state_font_size = state_font_size
        self.state_text_buffer = state_text_buffer
        self.label_side = label_side
        self.ax.set_title(self.title, fontsize=self.title_font_size)
        self._plot_states()

    def add_arrow(self, index, between, kind, label='', head_length=10, head_aspect=1, font_size=14, color='k'):
        x1, x2 = between
        y1 = self.energies[x1]
        y2 = self.energies[x2]
        dx = x2 - x1
        dy = y2 - y1
        arrow_style = f'-[{kind}]>' if kind in ['|', '-'] else f'-[{kind}]'
        self.ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle=arrow_style, color=color, shrinkA=0, shrinkB=0, patchA=None,
                         patchB=None, connectionstyle=f'arc3,rad={0.3*dy/dx if dx != 0 else 0}', head_length=head_length, headwidth=head_length*head_aspect))
        if label:
            mid_x = x1 + dx / 2
            mid_y = y1 + dy / 2
            self.ax.text(mid_x, mid_y, label, fontsize=font_size,
                         ha='center', va='center', color=color)

    def _plot_states(self):
        for i, energy in enumerate(self.energies):
            self.ax.plot(i, energy, 'o', markersize=10)
            if self.label_side == 'left':
                self.ax.text(i - self.state_text_buffer, energy,
                             self.state_names[i], fontsize=self.state_font_size, ha='right', va='center')
            elif self.label_side == 'right':
                self.ax.text(i + self.state_text_buffer, energy,
                             self.state_names[i], fontsize=self.state_font_size, ha='left', va='center')

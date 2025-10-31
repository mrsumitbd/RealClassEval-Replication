
class Subplot:

    def __init__(self, ax, energies, number_of_interactions=4, title='', title_font_size=16, state_names=None, virtual=[None], state_font_size=14, state_text_buffer=0.5, label_side='left'):
        self.ax = ax
        self.energies = energies
        self.number_of_interactions = number_of_interactions
        self.title = title
        self.title_font_size = title_font_size
        self.state_names = state_names if state_names is not None else [
            f"State {i}" for i in range(len(energies))]
        self.virtual = virtual
        self.state_font_size = state_font_size
        self.state_text_buffer = state_text_buffer
        self.label_side = label_side

        # Calculate x positions for each interaction
        self.xs = [i for i in range(self.number_of_interactions)]
        # Draw energy levels
        self.level_lines = []
        for i, (energy, name, virt) in enumerate(zip(self.energies, self.state_names, self.virtual)):
            for x in self.xs:
                if virt is not None and virt:
                    line = self.ax.plot(
                        [x - 0.3, x + 0.3], [energy, energy], 'k--', lw=1)
                else:
                    line = self.ax.plot(
                        [x - 0.3, x + 0.3], [energy, energy], 'k-', lw=2)
                self.level_lines.append(line)
            # Add state name
            if self.label_side == 'left':
                self.ax.text(self.xs[0] - self.state_text_buffer, energy, name,
                             va='center', ha='right', fontsize=self.state_font_size)
            else:
                self.ax.text(self.xs[-1] + self.state_text_buffer, energy,
                             name, va='center', ha='left', fontsize=self.state_font_size)
        # Set title
        if self.title:
            self.ax.set_title(self.title, fontsize=self.title_font_size)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.axis('off')

    def add_arrow(self, index, between, kind, label='', head_length=10, head_aspect=1, font_size=14, color='k'):
        # index: which x position (interaction)
        # between: tuple (from_state, to_state)
        # kind: 'up', 'down', 'double', etc.
        x = self.xs[index]
        y0 = self.energies[between[0]]
        y1 = self.energies[between[1]]
        dx = 0
        dy = y1 - y0
        if kind == 'up':
            self.ax.arrow(x, y0, dx, dy, head_width=0.1, head_length=head_length, length_includes_head=True,
                          fc=color, ec=color, overhang=0.3, lw=2, head_starts_at_zero=False)
        elif kind == 'down':
            self.ax.arrow(x, y1, dx, -dy, head_width=0.1, head_length=head_length, length_includes_head=True,
                          fc=color, ec=color, overhang=0.3, lw=2, head_starts_at_zero=False)
        elif kind == 'double':
            # Draw up and down arrows
            self.ax.arrow(x-0.05, y0, dx, dy, head_width=0.08, head_length=head_length, length_includes_head=True,
                          fc=color, ec=color, overhang=0.3, lw=2, head_starts_at_zero=False)
            self.ax.arrow(x+0.05, y1, dx, -dy, head_width=0.08, head_length=head_length, length_includes_head=True,
                          fc=color, ec=color, overhang=0.3, lw=2, head_starts_at_zero=False)
        # Add label
        if label:
            y_label = (y0 + y1) / 2
            self.ax.text(x + 0.15, y_label, label, va='center',
                         ha='left', fontsize=font_size, color=color)

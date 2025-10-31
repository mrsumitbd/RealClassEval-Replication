
class Subplot:

    def __init__(self, ax, energies, number_of_interactions=4, title='', title_font_size=16, state_names=None, virtual=[None], state_font_size=14, state_text_buffer=0.5, label_side='left'):
        '''Subplot.
        '''
        import numpy as np

        self.ax = ax
        self.energies = np.array(energies)
        self.n_states = len(self.energies)
        self.number_of_interactions = number_of_interactions
        self.title = title
        self.title_font_size = title_font_size
        self.state_names = state_names if state_names is not None else [
            f'{i}' for i in range(self.n_states)]
        self.virtual = virtual if virtual is not None else [None]
        self.state_font_size = state_font_size
        self.state_text_buffer = state_text_buffer
        self.label_side = label_side

        # Set up axis
        self.ax.set_xticks(range(self.number_of_interactions + 1))
        self.ax.set_xticklabels([])
        self.ax.set_yticks([])
        self.ax.set_xlim(-0.5, self.number_of_interactions + 0.5)
        self.ax.set_ylim(-0.1, 1.1)
        self.ax.set_title(self.title, fontsize=self.title_font_size)
        self.ax.axis('off')

        # Draw energy levels
        self.level_lines = []
        for i, (energy, name) in enumerate(zip(self.energies, self.state_names)):
            is_virtual = (i in self.virtual)
            color = 'r' if is_virtual else 'k'
            ls = '--' if is_virtual else '-'
            line = self.ax.hlines(energy, 0, self.number_of_interactions,
                                  colors=color, linestyles=ls, linewidth=2, zorder=1)
            self.level_lines.append(line)
            # Add state label
            if self.label_side == 'left':
                x_text = 0 - self.state_text_buffer
                ha = 'right'
            else:
                x_text = self.number_of_interactions + self.state_text_buffer
                ha = 'left'
            self.ax.text(
                x_text, energy, name,
                fontsize=self.state_font_size,
                va='center', ha=ha, color=color, zorder=2
            )

    def add_arrow(self, index, between, kind, label='', head_length=10, head_aspect=1, font_size=14, color='k'):
        '''Add an arrow to the WMEL diagram.
        '''
        import numpy as np
        from matplotlib.patches import FancyArrowPatch

        # index: can be int or (start, stop)
        if isinstance(index, (list, tuple, np.ndarray)) and len(index) == 2:
            x0, x1 = index
        else:
            x0 = x1 = index

        s0, s1 = between
        y0 = self.energies[s0]
        y1 = self.energies[s1]

        # Arrow direction and style
        if kind == 'ket':
            dx = x1 - x0
            dy = y1 - y0
            arrowstyle = '->'
        elif kind == 'bra':
            dx = x0 - x1
            dy = y0 - y1
            # swap start/end for bra
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            arrowstyle = '->'
        elif kind == 'outket':
            dx = x1 - x0
            dy = y1 - y0
            arrowstyle = '<-'
        elif kind == 'outbra':
            dx = x0 - x1
            dy = y0 - y1
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            arrowstyle = '<-'
        else:
            raise ValueError(
                "kind must be one of {'ket', 'bra', 'outbra', 'outket'}")

        # Draw line and arrow head
        line = self.ax.plot([x0, x1], [y0, y1], color=color, zorder=3)[0]
        # Arrow head
        arrow_head = FancyArrowPatch(
            (x0, y0), (x1, y1),
            arrowstyle=arrowstyle,
            mutation_scale=head_length,
            color=color,
            linewidth=2,
            zorder=4
        )
        self.ax.add_patch(arrow_head)

        # Label
        if label:
            xm = (x0 + x1) / 2
            ym = (y0 + y1) / 2
            # Offset label a bit perpendicular to the arrow
            dx = x1 - x0
            dy = y1 - y0
            length = np.hypot(dx, dy)
            if length == 0:
                perp = (0, 0.1)
            else:
                perp = (-dy / length, dx / length)
            offset = 0.08
            xm_off = xm + offset * perp[0]
            ym_off = ym + offset * perp[1]
            text = self.ax.text(
                xm_off, ym_off, label,
                fontsize=font_size,
                color=color,
                ha='center', va='center',
                zorder=5
            )
        else:
            text = None

        return [line, arrow_head, text]

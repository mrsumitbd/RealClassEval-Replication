import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import numpy as np


class Subplot:

    def __init__(self, ax, energies, number_of_interactions=4, title='', title_font_size=16, state_names=None, virtual=[None], state_font_size=14, state_text_buffer=0.5, label_side='left'):
        self.ax = ax
        self.energies = list(energies)
        self.n_states = len(self.energies)
        self.n_interactions = int(number_of_interactions)
        self.title = title
        self.title_font_size = title_font_size
        self.state_names = state_names if state_names is not None else [
            f"State {i}" for i in range(self.n_states)]
        self.virtual = set() if virtual is None else set(
            [v for v in virtual if v is not None])
        self.state_font_size = state_font_size
        self.state_text_buffer = float(state_text_buffer)
        self.label_side = label_side if label_side in (
            'left', 'right') else 'left'

        # Prepare axes
        self.ax.set_title(self.title, fontsize=self.title_font_size)
        self._draw_energy_levels()
        self._decorate_axes()

    def _draw_energy_levels(self):
        # Draw short horizontal ticks for each state at each interaction column
        xs = np.arange(self.n_interactions, dtype=float)
        tick_half_width = 0.35
        color_normal = 'k'
        color_virtual = '0.6'
        lw_normal = 2.0
        lw_virtual = 1.5
        ls_normal = '-'
        ls_virtual = '--'

        for s, E in enumerate(self.energies):
            is_virtual = s in self.virtual
            c = color_virtual if is_virtual else color_normal
            lw = lw_virtual if is_virtual else lw_normal
            ls = ls_virtual if is_virtual else ls_normal
            for x in xs:
                self.ax.plot([x - tick_half_width, x + tick_half_width],
                             [E, E], color=c, lw=lw, ls=ls, solid_capstyle='butt')

        # State labels
        if self.label_side == 'left':
            x_text = -self.state_text_buffer
            ha = 'right'
        else:
            x_text = (self.n_interactions - 1) + self.state_text_buffer
            ha = 'left'

        for s, E in enumerate(self.energies):
            txt = self.state_names[s] if s < len(
                self.state_names) else f"State {s}"
            self.ax.text(x_text, E, txt,
                         fontsize=self.state_font_size, va='center', ha=ha)

    def _decorate_axes(self):
        # Limits and cleanup
        x_margin_left = 1.0 if self.label_side == 'left' else 0.25
        x_margin_right = 1.0 if self.label_side == 'right' else 0.25
        self.ax.set_xlim(-x_margin_left,
                         (self.n_interactions - 1) + x_margin_right)

        if len(self.energies) > 0:
            e_min = min(self.energies)
            e_max = max(self.energies)
            e_pad = 0.05 * (e_max - e_min if e_max > e_min else 1.0)
            self.ax.set_ylim(e_min - e_pad, e_max + e_pad)

        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.yaxis.set_ticks_position('left')
        self.ax.xaxis.set_visible(False)
        self.ax.grid(False)

    def add_arrow(self, index, between, kind, label='', head_length=10, head_aspect=1, font_size=14, color='k'):
        # Resolve x position
        x = float(index)
        # Resolve states
        if not (isinstance(between, (list, tuple)) and len(between) == 2):
            raise ValueError(
                "between must be a tuple/list of two state indices (from_state, to_state)")
        i0, i1 = int(between[0]), int(between[1])
        if not (0 <= i0 < self.n_states and 0 <= i1 < self.n_states):
            raise IndexError("State indices out of range")
        y0 = float(self.energies[i0])
        y1 = float(self.energies[i1])

        # Determine arrow style
        k = (kind or '').lower()
        if k in ('up', 'absorption'):
            arrowstyle = '-|>'
            y_start, y_end = (min(y0, y1), max(y0, y1))
        elif k in ('down', 'emission'):
            arrowstyle = '<|-'
            y_start, y_end = (max(y0, y1), min(y0, y1))
        elif k in ('both', 'two-headed', 'double'):
            arrowstyle = '<|-|>'
            y_start, y_end = (min(y0, y1), max(y0, y1))
        else:
            # Default: point towards the actual target state i1
            if y1 > y0:
                arrowstyle = '-|>'
                y_start, y_end = (y0, y1)
            elif y1 < y0:
                arrowstyle = '<|-'
                y_start, y_end = (y0, y1)
            else:
                # Same energy: draw small horizontal arrow to the right
                dx = 0.6
                arrow = FancyArrowPatch(
                    (x - 0.3, y0),
                    (x + dx - 0.3, y0),
                    arrowstyle='-|>',
                    mutation_scale=max(2.0, float(
                        head_length) * float(head_aspect)),
                    linewidth=2.0,
                    color=color
                )
                self.ax.add_patch(arrow)
                if label:
                    self.ax.text(x + dx - 0.2, y0, label, fontsize=font_size,
                                 va='center', ha='left', color=color)
                return arrow

        # Line style
        ls = '--' if ('dash' in k or 'virtual' in k) else '-'
        ms = max(2.0, float(head_length) * float(head_aspect))

        arrow = FancyArrowPatch(
            (x, y_start),
            (x, y_end),
            arrowstyle=arrowstyle,
            mutation_scale=ms,
            linewidth=2.0,
            linestyle=ls,
            color=color
        )
        self.ax.add_patch(arrow)

        if label:
            y_mid = (y_start + y_end) / 2.0
            x_off = 0.15
            ha = 'left'
            self.ax.text(x + x_off, y_mid, label, fontsize=font_size,
                         va='center', ha=ha, color=color)

        return arrow

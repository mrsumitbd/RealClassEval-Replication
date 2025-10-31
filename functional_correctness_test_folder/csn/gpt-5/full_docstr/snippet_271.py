import numpy as np
from matplotlib.patches import FancyArrowPatch


class Subplot:
    '''Subplot containing WMEL.'''

    def __init__(self, ax, energies, number_of_interactions=4, title='', title_font_size=16, state_names=None, virtual=[None], state_font_size=14, state_text_buffer=0.5, label_side='left'):
        '''Subplot.
        Parameters
        ----------
        ax : matplotlib axis
            The axis.
        energies : 1D array-like
            Energies (scaled between 0 and 1)
        number_of_interactions : integer
            Number of interactions in diagram.
        title : string (optional)
            Title of subplot. Default is empty string.
        state_names: list of str (optional)
            list of the names of the states
        virtual: list of ints (optional)
            list of indexes of any vitual energy states
        state_font_size: numtype (optional)
            font size for the state lables
        state_text_buffer: numtype (optional)
            space between the energy level bars and the state labels
        '''
        self.ax = ax
        self.energies = np.asarray(energies, dtype=float)
        self.n_states = len(self.energies)
        self.n_interactions = int(number_of_interactions)
        self.state_names = state_names if state_names is not None else [
            f"|{i}>" for i in range(self.n_states)]
        self.virtual = set([] if virtual is None else virtual)
        self.state_font_size = state_font_size
        self.state_text_buffer = state_text_buffer
        self.label_side = label_side

        self.xmin = 0.0
        self.xmax = self.n_interactions + 1.0
        ypad = 0.05 * (self.energies.max() - self.energies.min() + 1e-9)
        self.ymin = self.energies.min() - ypad
        self.ymax = self.energies.max() + ypad

        # Draw horizontal energy levels
        for i, y in enumerate(self.energies):
            ls = '--' if (i in self.virtual) else '-'
            self.ax.plot([self.xmin, self.xmax], [
                         y, y], ls=ls, color='k', lw=1)

        # Labels on states
        if self.label_side == 'right':
            xlbl = self.xmax + self.state_text_buffer
            ha = 'left'
        else:
            xlbl = self.xmin - self.state_text_buffer
            ha = 'right'
        for i, y in enumerate(self.energies):
            self.ax.text(xlbl, y, str(
                self.state_names[i]), va='center', ha=ha, fontsize=self.state_font_size)

        # Optional vertical guides for interactions
        for i in range(1, self.n_interactions + 1):
            self.ax.axvline(i, color='0.8', lw=0.5, zorder=0)

        # Axes cosmetics
        self.ax.set_xlim(self.xmin - 1.0, self.xmax + 1.0)
        self.ax.set_ylim(self.ymin, self.ymax)
        self.ax.set_xticks(range(self.n_interactions + 1))
        self.ax.set_yticks([])
        self.ax.set_title(title, fontsize=title_font_size)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['top'].set_visible(False)

    def _kind_offset(self, kind):
        if kind == 'ket':
            return -0.15
        if kind == 'bra':
            return +0.15
        if kind == 'outket':
            return -(0.5 + 0.15)
        if kind == 'outbra':
            return (0.5 + 0.15)
        return 0.0

    def _arrow_head(self, x0, y0, x1, y1, color, head_length, head_aspect):
        vx = x1 - x0
        vy = y1 - y0
        norm = np.hypot(vx, vy)
        if norm == 0:
            vx, vy = 0.0, 1.0
            norm = 1.0
        # place a head using FancyArrowPatch; minimal shaft by making start very close to end
        eps = 1e-6
        xa = x1 - (vx / norm) * eps
        ya = y1 - (vy / norm) * eps
        head = FancyArrowPatch(
            (xa, ya),
            (x1, y1),
            arrowstyle='-|>',
            mutation_scale=head_length * max(0.1, head_aspect),
            color=color,
            lw=0,
            shrinkA=0,
            shrinkB=0,
            zorder=5,
            clip_on=False,
        )
        self.ax.add_patch(head)
        return head

    def add_arrow(self, index, between, kind, label='', head_length=10, head_aspect=1, font_size=14, color='k'):
        '''Add an arrow to the WMEL diagram.
        Parameters
        ----------
        index : integer
            The interaction, or start and stop interaction for the arrow.
        between : 2-element iterable of integers
            The inital and final state of the arrow
        kind : {'ket', 'bra', 'outbra', 'outket'}
            The kind of interaction.
        label : string (optional)
            Interaction label. Default is empty string.
        head_length: number (optional)
            size of arrow head
        font_size : number (optional)
            Label font size. Default is 14.
        color : matplotlib color (optional)
            Arrow color. Default is black.
        Returns
        -------
        [line,arrow_head,text]
        '''
        if not hasattr(between, '__len__') or len(between) != 2:
            raise ValueError(
                "between must be a 2-element iterable of state indices")
        s0, s1 = int(between[0]), int(between[1])
        y0 = float(self.energies[s0])
        y1 = float(self.energies[s1])

        # Determine x positions based on index and kind
        x_off = self._kind_offset(kind)
        if isinstance(index, (list, tuple, np.ndarray)) and len(index) == 2:
            x_start = float(index[0]) + x_off
            x_end = float(index[1]) + x_off
        elif np.isscalar(index):
            idx = float(index)
            # instantaneous interaction: vertical arrow at a single interaction line
            x_start = idx + x_off
            x_end = idx + x_off
        else:
            raise ValueError(
                "index must be an integer or a 2-element iterable")

        # Special handling for out-of-sequence arrows
        if kind == 'outket':
            x_start = self.xmin - 0.5
            if np.isscalar(index):
                x_end = x_start
        elif kind == 'outbra':
            x_start = self.xmax + 0.5
            if np.isscalar(index):
                x_end = x_start

        # Avoid zero-length arrows for instantaneous interactions by slightly offsetting y
        if x_start == x_end and y0 == y1:
            y1 = y0 + 0.02 * (self.ymax - self.ymin)

        line = self.ax.plot([x_start, x_end], [y0, y1],
                            color=color, lw=1.5, zorder=4)[0]
        head = self._arrow_head(x_start, y0, x_end, y1, color=color,
                                head_length=head_length, head_aspect=head_aspect)

        # Label placement near the midpoint, offset normal to arrow
        mx = 0.5 * (x_start + x_end)
        my = 0.5 * (y0 + y1)
        dx = x_end - x_start
        dy = y1 - y0
        nrm = np.hypot(dx, dy)
        if nrm == 0:
            nx, ny = 0.0, 1.0
        else:
            nx, ny = -dy / nrm, dx / nrm
        # Offset magnitude relative to axes ranges
        ox = nx * 0.03 * (self.xmax - self.xmin)
        oy = ny * 0.03 * (self.ymax - self.ymin)
        txt = self.ax.text(mx + ox, my + oy, label, color=color,
                           fontsize=font_size, ha='center', va='center')

        return [line, head, txt]

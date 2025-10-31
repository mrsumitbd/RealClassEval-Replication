class Subplot:

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
        import numpy as np
        import matplotlib.pyplot as plt

        self.ax = ax
        self.energies = np.asarray(energies, dtype=float)
        self.n_states = len(self.energies)
        self.n_interactions = int(number_of_interactions)
        self.title = title
        self.title_font_size = title_font_size
        self.state_names = state_names if state_names is not None else [
            str(i) for i in range(self.n_states)]
        self.virtual = set([] if virtual is None else (
            [] if virtual == [None] else list(virtual)))
        self.state_font_size = state_font_size
        self.state_text_buffer = float(state_text_buffer)
        self.label_side = label_side if label_side in (
            'left', 'right') else 'left'

        # X span of the energy level bars
        self.x_min = -0.5
        self.x_max = self.n_interactions + 0.5

        # Draw energy level lines
        self.level_lines = []
        for i, y in enumerate(self.energies):
            is_virtual = i in self.virtual
            ls = '--' if is_virtual else '-'
            lw = 1.5 if not is_virtual else 1.0
            c = 'k' if not is_virtual else '0.5'
            line, = ax.plot([self.x_min, self.x_max], [y, y],
                            linestyle=ls, color=c, lw=lw, zorder=1)
            self.level_lines.append(line)

        # Add state labels
        if self.label_side == 'left':
            x_label = self.x_min - self.state_text_buffer
            ha = 'right'
        else:
            x_label = self.x_max + self.state_text_buffer
            ha = 'left'

        self.state_texts = []
        for i, y in enumerate(self.energies):
            txt = ax.text(x_label, y, self.state_names[i], ha=ha, va='center',
                          fontsize=self.state_font_size, color=('0.35' if i in self.virtual else 'k'))
            self.state_texts.append(txt)

        # Styling axes
        ax.set_ylim(min(0.0, float(np.min(self.energies)) - 0.05),
                    max(1.0, float(np.max(self.energies)) + 0.05))
        ax.set_xlim(self.x_min - self.state_text_buffer - 0.2,
                    self.x_max + self.state_text_buffer + 0.2)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(left=False, bottom=False,
                       labelleft=False, labelbottom=False)

        # Title
        if self.title:
            ax.set_title(self.title, fontsize=self.title_font_size)

        # Storage for arrows
        self.arrows = []

    def _kind_offset(self, kind):
        # Horizontal offset to separate bra/ket arrows visually on the same interaction line
        if kind == 'ket':
            return +0.18
        if kind == 'bra':
            return -0.18
        if kind == 'outket':
            return +0.0
        if kind == 'outbra':
            return +0.0
        return 0.0

    def _x_from_index_and_kind(self, idx, kind):
        # Resolve x positions for a given index spec and kind
        if isinstance(idx, (list, tuple)) and len(idx) == 2:
            x0, x1 = float(idx[0]), float(idx[1])
            off0 = self._kind_offset(kind)
            off1 = self._kind_offset(kind)
            return x0 + off0, x1 + off1
        else:
            x = float(idx)
            off = self._kind_offset(kind)
            return x + off, x + off

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
        import numpy as np
        from matplotlib import patches

        # Validate inputs
        if kind not in ('ket', 'bra', 'outbra', 'outket'):
            raise ValueError(
                "kind must be one of {'ket','bra','outbra','outket'}")
        if not (isinstance(between, (list, tuple)) and len(between) == 2):
            raise ValueError(
                "between must be a 2-element iterable of integers (initial_state, final_state)")

        i0, i1 = int(between[0]), int(between[1])
        if not (0 <= i0 < self.n_states and 0 <= i1 < self.n_states):
            raise IndexError("state indices in 'between' are out of range")

        # Determine x positions
        # For outbra/outket, if index is not provided as a 2-tuple, map to outside positions
        if kind in ('outket', 'outbra') and not (isinstance(index, (list, tuple)) and len(index) == 2):
            if kind == 'outket':
                x0, x1 = self.n_interactions, self.n_interactions + 0.8
            else:
                x0, x1 = 0.0, -0.8
        else:
            x0, x1 = self._x_from_index_and_kind(index, kind)

        y0 = float(self.energies[i0])
        y1 = float(self.energies[i1])

        # Draw shaft as a simple line
        line = self.ax.plot([x0, x1], [y0, y1],
                            color=color, lw=2.0, zorder=3)[0]

        # Arrow head
        # Compute arrow head orientation
        dx = x1 - x0
        dy = y1 - y0
        length = np.hypot(dx, dy) if (dx != 0 or dy != 0) else 1.0
        if length == 0:
            ux, uy = 1.0, 0.0
        else:
            ux, uy = dx / length, dy / length

        # head size scales in data coordinates
        # Use head_length in points converted approximately to data units using axis transforms
        # Fallback: scale head length relative to x-span
        xspan = max(1e-6, self.ax.get_xlim()[1] - self.ax.get_xlim()[0])
        yspan = max(1e-6, self.ax.get_ylim()[1] - self.ax.get_ylim()[0])
        # Convert head_length (points) to data approx: assume 72 dpi and figure size; fallback to small fraction
        # Use a fraction of spans for robustness
        head_len_data = 0.03 * np.hypot(xspan, yspan) * (head_length / 10.0)
        head_width_data = head_len_data * (0.6 / max(1e-6, head_aspect))

        # Triangle points for the head at end (x1, y1)
        left_x = x1 - ux * head_len_data - uy * head_width_data
        left_y = y1 - uy * head_len_data + ux * head_width_data
        right_x = x1 - ux * head_len_data + uy * head_width_data
        right_y = y1 - uy * head_len_data - ux * head_width_data

        arrow_head = patches.Polygon([[x1, y1], [left_x, left_y], [right_x, right_y]],
                                     closed=True, facecolor=color, edgecolor=color, zorder=4)
        self.ax.add_patch(arrow_head)

        # Label
        text_obj = None
        if label:
            mx = (x0 + x1) / 2.0
            my = (y0 + y1) / 2.0
            # Offset label slightly perpendicular to the arrow direction
            nx, ny = -uy, ux
            label_offset = 0.02 * np.hypot(xspan, yspan)
            tx = mx + nx * label_offset
            ty = my + ny * label_offset
            ha = 'left' if dx >= 0 else 'right'
            text_obj = self.ax.text(tx, ty, label, fontsize=font_size, color=color,
                                    ha=ha, va='center', zorder=5)

        self.arrows.append((line, arrow_head, text_obj))
        return [line, arrow_head, text_obj]

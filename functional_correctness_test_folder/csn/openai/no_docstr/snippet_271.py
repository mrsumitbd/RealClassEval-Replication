
import numpy as np
import matplotlib.pyplot as plt


class Subplot:
    """
    A simple helper class to draw energy level diagrams with arrows between states.
    """

    def __init__(
        self,
        ax,
        energies,
        number_of_interactions=4,
        title="",
        title_font_size=16,
        state_names=None,
        virtual=[None],
        state_font_size=14,
        state_text_buffer=0.5,
        label_side="left",
    ):
        """
        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axis on which to draw the diagram.
        energies : list or array-like
            Energy values for each state (in arbitrary units).
        number_of_interactions : int, optional
            Number of interaction levels to display (default 4).
        title : str, optional
            Title of the subplot.
        title_font_size : int, optional
            Font size of the title.
        state_names : list of str, optional
            Names for each state. If None, default names are used.
        virtual : list, optional
            List of virtual states (currently unused).
        state_font_size : int, optional
            Font size for state labels.
        state_text_buffer : float, optional
            Horizontal buffer for state labels.
        label_side : {'left', 'right'}, optional
            Side on which to place state labels.
        """
        self.ax = ax
        self.energies = np.asarray(energies, dtype=float)
        self.n_states = len(self.energies)
        self.number_of_interactions = number_of_interactions
        self.title = title
        self.title_font_size = title_font_size
        self.state_names = (
            state_names if state_names is not None else [
                f"S{i}" for i in range(self.n_states)]
        )
        self.virtual = virtual
        self.state_font_size = state_font_size
        self.state_text_buffer = state_text_buffer
        self.label_side = label_side

        # Compute y positions (equally spaced)
        self.y_positions = np.arange(self.n_states)

        # Draw horizontal lines for each state
        for i, y in enumerate(self.y_positions):
            self.ax.hlines(
                y,
                xmin=0,
                xmax=1,
                color="k",
                linewidth=1.5,
                label=self.state_names[i] if i == 0 else None,
            )

        # Label states
        for i, y in enumerate(self.y_positions):
            if self.label_side == "left":
                ha = "right"
                x = -self.state_text_buffer
            else:
                ha = "left"
                x = 1 + self.state_text_buffer
            self.ax.text(
                x,
                y,
                self.state_names[i],
                ha=ha,
                va="center",
                fontsize=self.state_font_size,
            )

        # Set title
        if self.title:
            self.ax.set_title(self.title, fontsize=self.title_font_size)

        # Set limits and hide ticks
        self.ax.set_xlim(-0.2, 1.2)
        self.ax.set_ylim(-0.5, self.n_states - 0.5)
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        # Store arrows for potential future reference
        self.arrows = []

    def add_arrow(
        self,
        index,
        between,
        kind,
        label="",
        head_length=10,
        head_aspect=1,
        font_size=14,
        color="k",
    ):
        """
        Draw an arrow between two states.

        Parameters
        ----------
        index : int
            Index of the starting state.
        between : int
            Index of the ending state.
        kind : str
            Type of transition (currently unused, but can be used to style arrows).
        label : str, optional
            Text label to place near the arrow.
        head_length : float, optional
            Length of the arrow head in points.
        head_aspect : float, optional
            Aspect ratio of the arrow head.
        font_size : int, optional
            Font size of the label.
        color : str, optional
            Color of the arrow.
        """
        if not (0 <= index < self.n_states and 0 <= between < self.n_states):
            raise ValueError("State indices out of range.")

        y_start = self.y_positions[index]
        y_end = self.y_positions[between]

        # Determine arrow direction
        if y_start < y_end:
            # Upward arrow
            xy_start = (0.5, y_start)
            xy_end = (0.5, y_end)
        else:
            # Downward arrow
            xy_start = (0.5, y_start)
            xy_end = (0.5, y_end)

        # Arrow properties
        arrowprops = dict(
            arrowstyle="->",
            color=color,
            lw=1.5,
            head_width=head_length * head_aspect / 72.0,  # convert points to inches
            head_length=head_length / 72.0,
            shrinkA=0,
            shrinkB=0,
        )

        # Draw arrow
        self.ax.annotate(
            "",
            xy=xy_end,
            xytext=xy_start,
            arrowprops=arrowprops,
            va="center",
            ha="center",
        )

        # Add label if provided
        if label:
            mid_y = (y_start + y_end) / 2
            self.ax.text(
                0.5,
                mid_y,
                label,
                fontsize=font_size,
                ha="center",
                va="center",
                color=color,
            )

        # Store arrow info
        self.arrows.append(
            {
                "start": index,
                "end": between,
                "kind": kind,
                "label": label,
                "color": color,
            }
        )

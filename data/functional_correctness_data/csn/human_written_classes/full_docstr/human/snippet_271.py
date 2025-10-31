import numpy as np

class Subplot:
    """Subplot containing WMEL."""

    def __init__(self, ax, energies, number_of_interactions=4, title='', title_font_size=16, state_names=None, virtual=[None], state_font_size=14, state_text_buffer=0.5, label_side='left'):
        """Subplot.

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
        """
        self.ax = ax
        self.energies = energies
        self.interactions = number_of_interactions
        self.state_names = state_names
        for i in range(len(self.energies)):
            if i in virtual:
                linestyle = '--'
            else:
                linestyle = '-'
            self.ax.axhline(self.energies[i], color='k', linewidth=2, ls=linestyle, zorder=5)
        if isinstance(state_names, list):
            for i in range(len(self.energies)):
                if label_side == 'left':
                    ax.text(-state_text_buffer, energies[i], state_names[i], fontsize=state_font_size, verticalalignment='center', horizontalalignment='center')
                elif label_side == 'right':
                    ax.text(1 + state_text_buffer, energies[i], state_names[i], fontsize=state_font_size, verticalalignment='center', horizontalalignment='center')
        self.x_pos = np.linspace(0, 1, number_of_interactions)
        self.ax.set_xlim(-0.1, 1.1)
        self.ax.set_ylim(-0.01, 1.01)
        self.ax.axis('off')
        self.ax.set_title(title, fontsize=title_font_size)

    def add_arrow(self, index, between, kind, label='', head_length=10, head_aspect=1, font_size=14, color='k'):
        """Add an arrow to the WMEL diagram.

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
        """
        if hasattr(index, 'index'):
            x_pos = list(index)
        else:
            x_pos = [index] * 2
        x_pos = [np.linspace(0, 1, self.interactions)[i] for i in x_pos]
        y_pos = [self.energies[between[0]], self.energies[between[1]]]
        arrow_length = self.energies[between[1]] - self.energies[between[0]]
        arrow_end = self.energies[between[1]]
        if arrow_length > 0:
            direction = 1
        elif arrow_length < 0:
            direction = -1
        else:
            raise ValueError('between invalid!')
        length = abs(y_pos[0] - y_pos[1])
        if kind == 'ket':
            line = self.ax.plot(x_pos, y_pos, linestyle='-', color=color, linewidth=2, zorder=9)
        elif kind == 'bra':
            line = self.ax.plot(x_pos, y_pos, linestyle='--', color=color, linewidth=2, zorder=9)
        elif kind == 'out':
            yi = np.linspace(y_pos[0], y_pos[1], 100)
            xi = np.sin((yi - y_pos[0]) * int(1 / length * 20) * 2 * np.pi * length) / 40 + x_pos[0]
            line = self.ax.plot(xi[:-5], yi[:-5], linestyle='-', color=color, linewidth=2, solid_capstyle='butt', zorder=9)
        elif kind == 'outbra':
            yi = np.linspace(y_pos[0], y_pos[1], 100)
            xi = np.sin((yi - y_pos[0]) * int(1 / length * 20) * 2 * np.pi * length) / 40 + x_pos[0]
            counter = 0
            while counter - 13 <= len(yi):
                subyi = yi[counter:counter + 15]
                subxi = xi[counter:counter + 15]
                line = self.ax.plot(subxi[:-5], subyi[:-5], linestyle='-', color=color, linewidth=2, solid_capstyle='butt', zorder=9)
                counter += 13
        else:
            raise ValueError("kind is not 'ket', 'bra', 'out' or 'outbra'.")
        dx = x_pos[1] - x_pos[0]
        dy = y_pos[1] - y_pos[0]
        xytext = (x_pos[1] - dx * 0.01, y_pos[1] - dy * 0.01)
        annotation = self.ax.annotate('', xy=(x_pos[1], y_pos[1]), xytext=xytext, arrowprops=dict(fc=color, ec=color, shrink=0, headwidth=head_length * head_aspect, headlength=head_length, linewidth=0, zorder=10), size=25)
        text = self.ax.text(np.mean(x_pos), -0.15, label, fontsize=font_size, horizontalalignment='center')
        return (line, annotation.arrow_patch, text)
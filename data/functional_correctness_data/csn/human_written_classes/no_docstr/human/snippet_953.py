class Focus:

    def __init__(self, axes, sliders, linewidth=2):
        self.axes = axes
        self.sliders = sliders
        self.linewidth = linewidth
        ax = axes[0]
        for side in ['top', 'bottom', 'left', 'right']:
            ax.spines[side].set_linewidth(self.linewidth)
        self.focus_axis = ax

    def __call__(self, ax):
        if type(ax) == str:
            ind = self.axes.index(self.focus_axis)
            if ax == 'next':
                ind -= 1
            elif ax == 'previous':
                ind += 1
            ax = self.axes[ind % len(self.axes)]
        if self.focus_axis == ax or ax not in self.axes:
            return
        else:
            if self.focus_axis.get_gid() in self.sliders.keys():
                self.sliders[self.focus_axis.get_gid()].track.set_facecolor('lightgrey')
            if ax.get_gid() in self.sliders.keys():
                self.sliders[ax.get_gid()].track.set_facecolor('darkgrey')
            for spine in ['top', 'bottom', 'left', 'right']:
                self.focus_axis.spines[spine].set_linewidth(1)
                ax.spines[spine].set_linewidth(self.linewidth)
            self.focus_axis = ax
class OrbitPlotSet:
    """
    Class for visualizing simulations using instantaneous orbits in 3D. Uses three rebound.OrbitPlot instances internally.
    """

    def __init__(self, sim, slices=0.5, fig=None, ax=None, figsize=(5, 8), unitlabel=None, **kwargs):
        """
        Initializer for OrbitPlotSet class

        This function has the same arguments as OrbitPlot() with the addition of:

        Parameters
        ----------
        slices            : float, optional
            Changes the height and width of the top and right plot relative to the main plot. Default: 0.5.
        """
        try:
            import matplotlib.pyplot as plt
            from mpl_toolkits.axes_grid1 import make_axes_locatable
        except:
            raise ImportError("Error importing matplotlib and/or numpy. Plotting functions not available. If running from within a jupyter notebook, try calling '%matplotlib inline' beforehand.")
        updateLimits = True
        if fig is not None:
            updateLimits = False
            self.fig = fig
            self.ax_main, self.ax_top, self.ax_right = ax
        else:
            if unitlabel is not None:
                unitlabel = ' ' + unitlabel
            else:
                unitlabel = ''
            self.fig = plt.figure(figsize=figsize)
            self.ax_main = plt.subplot(111, aspect='equal')
            self.ax_main.set_xlabel('x' + unitlabel)
            self.ax_main.set_ylabel('y' + unitlabel)
            divider = make_axes_locatable(self.ax_main)
            divider.set_aspect(True)
            self.ax_top = divider.append_axes('top', size='%.2f%%' % (100.0 * slices), sharex=self.ax_main, pad=0)
            self.ax_top.set_aspect('equal', adjustable='datalim')
            self.ax_right = divider.append_axes('right', size='%.2f%%' % (100.0 * slices), sharey=self.ax_main, pad=0)
            self.ax_right.set_aspect('equal', adjustable='datalim')
            plt.setp(self.ax_top.get_xticklabels(), visible=False)
            plt.setp(self.ax_top.get_xticklines(), visible=False)
            self.ax_top.set_ylabel('z' + unitlabel)
            plt.setp(self.ax_right.get_yticklabels(), visible=False)
            plt.setp(self.ax_right.get_yticklines(), visible=False)
            self.ax_right.set_xlabel('z' + unitlabel)
        self.sim = sim
        self.main = OrbitPlot(sim, fig=self.fig, ax=self.ax_main, projection='xy', **kwargs)
        self.top = OrbitPlot(sim, fig=self.fig, ax=self.ax_top, projection='xz', **kwargs)
        self.right = OrbitPlot(sim, fig=self.fig, ax=self.ax_right, projection='zy', **kwargs)
        self.draw(updateLimits=updateLimits, update=True)

    def draw(self, update=False, updateLimits=True):
        self.main.draw(update=update, updateLimits=updateLimits)
        self.top.draw(update=update, updateLimits=updateLimits)
        self.right.draw(update=update, updateLimits=updateLimits)

    def update(self, updateLimits=True):
        self.main.update(updateLimits=updateLimits)
        self.top.update(updateLimits=updateLimits)
        self.right.update(updateLimits=updateLimits)
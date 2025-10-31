class GamutViewer2D:

    def __init__(self, ax, highlight_point_model, uniform_space, ap_lim=(-50, 50), bp_lim=(-50, 50)):
        self.ax = ax
        self.highlight_point_model = highlight_point_model
        self.ap_lim = ap_lim
        self.bp_lim = bp_lim
        self.uniform_space = uniform_space
        self.bgcolors = {'light': (0.9, 0.9, 0.9), 'dark': (0.1, 0.1, 0.1)}
        self.bgcolor_ranges = {'light': (0, 60), 'dark': (40, 100)}
        self.bg_opposites = {'light': 'dark', 'dark': 'light'}
        self.bg = 'light'
        self.ax.set_facecolor(self.bgcolors[self.bg])
        self.image = self.ax.imshow([[[0, 0, 0]]], aspect='equal', extent=ap_lim + bp_lim, origin='lower')
        self.highlight_point_model.trigger.add_callback(self._refresh)

    def _refresh(self):
        Jp, _, _ = self.highlight_point_model.get_Jpapbp()
        low, high = self.bgcolor_ranges[self.bg]
        if not low <= Jp <= high:
            self.bg = self.bg_opposites[self.bg]
            self.ax.set_facecolor(self.bgcolors[self.bg])
        sRGB = sRGB_gamut_Jp_slice(Jp, self.uniform_space, self.ap_lim, self.bp_lim)
        self.image.set_data(sRGB)
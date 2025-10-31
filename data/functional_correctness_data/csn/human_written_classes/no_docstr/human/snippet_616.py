import numpy as np

class CMapView:

    def __init__(self, ax, cmap_model):
        self.ax = ax
        self.cmap_model = cmap_model
        rgb_display, oog_display = self._drawable_arrays()
        self.image = self.ax.imshow(rgb_display, extent=(0, 0.2, 0, 1), origin='lower')
        self.gamut_alert_image = self.ax.imshow(oog_display, extent=(0.05, 0.15, 0, 1), origin='lower')
        self.ax.set_xlim(0, 0.2)
        self.ax.set_ylim(0, 1)
        self.ax.get_xaxis().set_visible(False)
        self.cmap_model.trigger.add_callback(self._refresh)

    def _drawable_arrays(self):
        rgb, oog = self.cmap_model.get_sRGB()
        rgb_display = rgb[:, np.newaxis, :]
        oog_display = np.empty((rgb.shape[0], 1, 4))
        oog_display[...] = [0, 0, 0, 0]
        oog_display[oog, :, :] = [0, 1, 1, 1]
        return (rgb_display, oog_display)

    def _refresh(self):
        rgb_display, oog_display = self._drawable_arrays()
        self.image.set_data(rgb_display)
        self.gamut_alert_image.set_data(oog_display)
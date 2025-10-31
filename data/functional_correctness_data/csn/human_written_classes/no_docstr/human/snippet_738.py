import warnings

class NotebookPlottingMixin:

    def _run_in_tileserver(self, capture):
        TileServer.run_tileserver(self, self.envelope)
        mp = TileServer.folium_client(self, self.envelope, capture=capture)
        return mp._repr_html_()

    def _repr_html_(self):
        from telluric.collections import BaseCollection
        from telluric.features import GeoFeature
        if isinstance(self, BaseCollection) and self[0].has_raster:
            return self._run_in_tileserver(capture='Feature collection of rasters')
        elif isinstance(self, GeoFeature) and self.has_raster:
            return self._run_in_tileserver(capture='GeoFeature with raster')
        warnings.warn('Plotting a limited representation of the data, use the .plot() method for further customization')
        return simple_plot(self)._repr_html_()

    def plot(self, mp=None, **plot_kwargs):
        return plot(self, mp, **plot_kwargs)
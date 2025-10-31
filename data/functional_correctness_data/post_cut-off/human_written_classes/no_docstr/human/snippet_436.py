from eubi_bridge.utils.convenience import sensitive_glob, is_zarr_group, is_zarr_array, take_filepaths, autocompute_chunk_shape
from eubi_bridge.ngff.multiscales import Pyramid

class NGFFImageMeta:

    def __init__(self, path):
        if is_zarr_group(path):
            self.pyr = Pyramid().from_ngff(path)
            meta = self.pyr.meta
            self._meta = meta
            self._base_path = self._meta.resolution_paths[0]
        else:
            raise Exception(f'The given path does not contain an NGFF group.')

    def get_axes(self):
        return self._meta.axis_order

    def get_scales(self):
        return self._meta.get_scale(self._base_path)

    def get_scaledict(self):
        return self._meta.get_scaledict(self._base_path)

    def get_units(self):
        return self._meta.unit_list

    def get_unitdict(self):
        return self._meta.unit_dict

    def get_channels(self):
        if not hasattr(self._meta, 'channels'):
            return None
        return self._meta.channels
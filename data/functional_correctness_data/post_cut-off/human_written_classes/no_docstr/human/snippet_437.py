from eubi_bridge.base.readers import read_metadata_via_bioio_bioformats, read_metadata_via_extension, read_metadata_via_bfio
from ome_types.model import OME, Image, Pixels, Channel

class PFFImageMeta:
    essential_omexml_fields = {'physical_size_x', 'physical_size_x_unit', 'physical_size_y', 'physical_size_y_unit', 'physical_size_z', 'physical_size_z_unit', 'time_increment', 'time_increment_unit', 'size_x', 'size_y', 'size_z', 'size_t', 'size_c'}

    def __init__(self, path, series, meta_reader='bioio'):
        if path.endswith('ome') or path.endswith('xml'):
            from ome_types import OME
            omemeta = OME().from_xml(path)
        elif meta_reader == 'bioio':
            try:
                omemeta = read_metadata_via_extension(path, series=series)
            except:
                omemeta = read_metadata_via_bioio_bioformats(path, series=series)
        elif meta_reader == 'bfio':
            try:
                omemeta = read_metadata_via_bfio(path)
            except:
                omemeta = read_metadata_via_bioio_bioformats(path, series=series)
        else:
            raise ValueError(f'Unsupported metadata reader: {meta_reader}')
        if series is None:
            series = 0
        images = [omemeta.images[series]]
        omemeta.images = images
        self.omemeta = omemeta
        self.pixels = self.omemeta.images[0].pixels
        missing_fields = self.essential_omexml_fields - self.pixels.model_fields_set
        self.pixels.model_fields_set.update(missing_fields)
        self.omemeta.images[0].pixels = self.pixels
        self.pyr = None

    def get_axes(self):
        return 'tczyx'

    def get_scaledict(self):
        return {'t': self.pixels.time_increment, 'z': self.pixels.physical_size_z, 'y': self.pixels.physical_size_y, 'x': self.pixels.physical_size_x}

    def get_scales(self):
        scaledict = self.get_scaledict()
        caxes = [ax for ax in self.get_axes() if ax != 'c']
        return [scaledict[ax] for ax in caxes]

    def get_unitdict(self):
        return {'t': self.pixels.time_increment_unit.name.lower(), 'z': self.pixels.physical_size_z_unit.name.lower(), 'y': self.pixels.physical_size_y_unit.name.lower(), 'x': self.pixels.physical_size_x_unit.name.lower()}

    def get_units(self):
        unitdict = self.get_unitdict()
        caxes = [ax for ax in self.get_axes() if ax != 'c']
        return [unitdict[ax] for ax in caxes]

    def get_channels(self):
        if not hasattr(self.pixels, 'channels'):
            return None
        if len(self.pixels.channels) == 0:
            return None
        if len(self.pixels.channels) < self.pixels.size_c:
            chn = ChannelIterator(num_channels=self.pixels.size_c)
            channels = chn._channels
        elif len(self.pixels.channels) == self.pixels.size_c:
            channels = []
            for _, channel in enumerate(self.pixels.channels):
                color = channel.color.as_hex().upper()
                color = expand_hex_shorthand(color)
                name = channel.name
                channels.append(dict(label=name, color=color))
        return channels
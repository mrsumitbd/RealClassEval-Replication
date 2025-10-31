from pyowm.commons.image import Image
from pyowm.commons.tile import Tile
from pyowm.utils import formatting

class SatelliteImage:
    """
    Class representing a downloaded satellite image, featuring both metadata and data

    :param metadata: the metadata for this satellite image
    :type metadata: a `pyowm.agro10.imagery.MetaImage` subtype instance
    :param data: the actual data for this satellite image
    :type data: either `pyowm.commons.image.Image` or `pyowm.commons.tile.Tile` object
    :param downloaded_on: the UNIX epoch this satellite image was downloaded at
    :type downloaded_on: int or `None`
    :param palette: ID of the color palette of the downloaded images. Values are provided by `pyowm.agroapi10.enums.PaletteEnum`
    :type palette: str or `None`
    :returns: a `pyowm.agroapi10.imagery.SatelliteImage` instance
    """

    def __init__(self, metadata, data, downloaded_on=None, palette=None):
        assert isinstance(metadata, MetaImage)
        self.metadata = metadata
        assert isinstance(data, (Image, Tile))
        self.data = data
        if downloaded_on is not None:
            assert isinstance(downloaded_on, int)
            self._downloaded_on = downloaded_on
        if palette is not None:
            assert isinstance(palette, str)
            self.palette = palette

    def downloaded_on(self, timeformat='unix'):
        """Returns the UTC time telling when the satellite image was downloaded from the OWM Agro API

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: an int or a str

        """
        return formatting.timeformat(self._downloaded_on, timeformat)

    def persist(self, path_to_file):
        """
        Saves the satellite image to disk on a file

        :param path_to_file: path to the target file
        :type path_to_file: str
        :return: `None`
        """
        self.data.persist(path_to_file)

    def __repr__(self):
        return '<%s.%s - %s %s satellite image downloaded on: %s>' % (__name__, self.__class__.__name__, self.metadata.preset, self.metadata.satellite_name, self.downloaded_on('iso') if self._downloaded_on is not None else 'None')
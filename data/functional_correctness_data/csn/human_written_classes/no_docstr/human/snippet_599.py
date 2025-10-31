import rasterio
from tempfile import NamedTemporaryFile
from mapchete.path import MPath, MPathLike
from typing import Generator, Optional, Union
from rasterio.io import DatasetWriter, MemoryFile, BufferedDatasetWriter

class RasterioRemoteTempFileWriter:
    path: MPath
    _sink: Union[BufferedDatasetWriter, DatasetWriter]

    def __init__(self, path: MPathLike, *args, **kwargs):
        logger.debug('open RasterioTempFileWriter for path %s', path)
        self.path = MPath.from_inp(path)
        self.fs = self.path.fs
        self._dst = NamedTemporaryFile(suffix=self.path.suffix)
        self._open_args = args
        self._open_kwargs = kwargs
        self._sink = None

    def __enter__(self):
        self._sink = rasterio.open(self._dst.name, 'w+', *self._open_args, **self._open_kwargs)
        return self._sink

    def __exit__(self, exc_type, exc_value, exc_traceback):
        try:
            self._sink.close()
            if exc_value is None:
                logger.debug('upload TempFile %s to %s', self._dst.name, self.path)
                self.fs.put_file(self._dst.name, self.path)
        finally:
            logger.debug('close and remove tempfile')
            self._dst.close()
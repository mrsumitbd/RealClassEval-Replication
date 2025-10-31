from typing import Generator, Optional, Union
from rasterio.io import DatasetWriter, MemoryFile, BufferedDatasetWriter
from mapchete.path import MPath, MPathLike

class RasterioRemoteMemoryWriter:
    path: MPath
    _sink: Union[BufferedDatasetWriter, DatasetWriter]

    def __init__(self, path: MPathLike, *args, **kwargs):
        logger.debug('open RasterioRemoteMemoryWriter for path %s', path)
        self.path = MPath.from_inp(path)
        self.fs = self.path.fs
        self._dst = MemoryFile()
        self._open_args = args
        self._open_kwargs = kwargs
        self._sink = None

    def __enter__(self):
        self._sink = self._dst.open(*self._open_args, **self._open_kwargs)
        return self._sink

    def __exit__(self, exc_type, exc_value, exc_traceback):
        try:
            self._sink.close()
            if exc_value is None:
                logger.debug('upload rasterio MemoryFile to %s', self.path)
                with self.fs.open(self.path, 'wb') as dst:
                    dst.write(self._dst.getbuffer())
        finally:
            logger.debug('close rasterio MemoryFile')
            self._dst.close()
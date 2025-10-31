
import rasterio


class RIOTag:
    """
    A simple wrapper around rasterio to manipulate tags for a given dataset.
    """

    def __init__(self, rfile, name):
        """
        Open the raster file and store the tag group name.

        Parameters
        ----------
        rfile : str or rasterio.io.DatasetReader
            Path to the raster file or an already opened rasterio dataset.
        name : str
            The tag group name to work with.
        """
        # If a path is provided, open the dataset in read/write mode.
        if isinstance(rfile, str):
            self._dataset = rasterio.open(rfile, mode='r+')
            self._own_dataset = True
        else:
            # Assume an already opened dataset is passed.
            self._dataset = rfile
            self._own_dataset = False

        self.name = name

    def __setitem__(self, key, item):
        """
        Set a tag key/value pair in the specified tag group.

        Parameters
        ----------
        key : str
            Tag key.
        item : str
            Tag value.
        """
        # Update the tags for the specified group.
        self._dataset.update_tags(name=self.name, **{key: str(item)})

    def close(self):
        """
        Close the raster file if it was opened by this instance.
        """
        if self._own_dataset:
            self._dataset.close()

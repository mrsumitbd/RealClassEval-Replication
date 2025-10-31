
import rasterio
import numpy as np
import base64
import io


class RIOTag:
    '''Rasterio wrapper to allow da.store on tag.'''

    def __init__(self, rfile, name):
        '''Init the rasterio tag.'''
        self.rfile = rfile
        self.name = name
        # Open the file in read/write mode
        self.r = rasterio.open(rfile, mode='r+')

    def __setitem__(self, key, item):
        '''Put the data in the tag.'''
        # Convert the array to a base64 encoded string
        buf = io.BytesIO()
        np.save(buf, item, allow_pickle=False)
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode('ascii')

        # Retrieve existing tags for the band
        tags = self.r.tags(self.name)
        # Update the tag dictionary
        tags[key] = b64
        # Write back the updated tags
        self.r.update_tags(self.name, **tags)

    def close(self):
        '''Close the file.'''
        self.r.close()

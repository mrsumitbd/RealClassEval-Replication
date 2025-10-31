
class RIOTag:
    '''Rasterio wrapper to allow da.store on tag.'''

    def __init__(self, rfile, name):
        '''Init the rasterio tag.'''
        self.rfile = rfile
        self.name = name

    def __setitem__(self, key, item):
        '''Put the data in the tag.'''
        # key is ignored, as tags are set by name
        self.rfile.update_tag(**{self.name: item})

    def close(self):
        '''Close the file.'''
        self.rfile.close()

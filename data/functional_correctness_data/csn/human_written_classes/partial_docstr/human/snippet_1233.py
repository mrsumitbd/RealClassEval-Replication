class FITSKeyExtractor:
    """Extract values from FITS images"""

    def __init__(self, values):
        self.map = {}
        for key, entry in values.items():
            if isinstance(entry, KeyDefinition):
                newval = entry
            elif isinstance(entry, tuple):
                if len(entry) == 3:
                    keyname = entry[0]
                    hduname = entry[1]
                    convert = entry[2]
                    default = None
                elif len(entry) == 2:
                    keyname = entry[0]
                    default = entry[1]
                    hduname = 0
                    convert = None
                else:
                    raise ValueError(f'a tuple in FITSKeyExtractor must have 2-3 fields, has {len(entry)} instead')
                newval = KeyDefinition(keyname, ext=hduname, convert=convert, default=default)
            elif isinstance(entry, str):
                newval = KeyDefinition(entry)
            else:
                newval = entry
            self.map[key] = newval

    def extract(self, value, hdulist):
        extractor = self.map[value]
        return extractor(hdulist)
class SemiMinorRadius:
    proj4 = '+b'

    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return '%s=%s' % (self.proj4, self.value)

    def to_esri_wkt(self):
        return str(self.value)

    def to_ogc_wkt(self):
        return str(self.value)
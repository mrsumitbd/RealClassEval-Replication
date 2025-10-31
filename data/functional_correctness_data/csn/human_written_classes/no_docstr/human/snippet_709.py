class FalseEasting:
    proj4 = '+x_0'
    esri_wkt = 'False_Easting'
    ogc_wkt = 'false_easting'
    geotiff = 'FalseEasting'

    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return '+x_0=%s' % self.value

    def to_ogc_wkt(self):
        return 'PARAMETER["false_easting", %s]' % self.value

    def to_esri_wkt(self):
        return 'PARAMETER["False_Easting", %s]' % self.value
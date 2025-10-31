class FalseNorthing:
    proj4 = '+y_0'
    esri_wkt = 'False_Northing'
    ogc_wkt = 'false_northing'
    geotiff = 'FalseNorthing'

    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return '+y_0=%s' % self.value

    def to_ogc_wkt(self):
        return 'PARAMETER["false_northing", %s]' % self.value

    def to_esri_wkt(self):
        return 'PARAMETER["False_Northing", %s]' % self.value
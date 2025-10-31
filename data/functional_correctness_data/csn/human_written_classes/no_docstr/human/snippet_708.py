class Azimuth:
    proj4 = '+alpha'
    esri_wkt = 'azimuth'
    ogc_wkt = 'azimuth'
    geotiff = 'AzimuthAngle'

    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return '+alpha=%s' % self.value

    def to_ogc_wkt(self):
        return 'PARAMETER["Azimuth",%s]' % self.value

    def to_esri_wkt(self):
        return 'PARAMETER["Azimuth",%s]' % self.value
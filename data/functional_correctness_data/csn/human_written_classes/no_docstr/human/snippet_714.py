class SatelliteHeight:
    proj4 = '+h'
    ogc_wkt = 'satellite_height'
    esri_wkt = 'satellite_height'

    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return '+h=%s' % self.value

    def to_ogc_wkt(self):
        return 'PARAMETER["satellite_height", %s]' % self.value

    def to_esri_wkt(self):
        return 'PARAMETER["satellite_height", %s]' % self.value
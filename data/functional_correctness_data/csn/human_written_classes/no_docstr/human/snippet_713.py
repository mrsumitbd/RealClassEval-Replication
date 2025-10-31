class LongitudeCenter:
    proj4 = '+lonc'
    ogc_wkt = 'Longitude_Of_Center'
    esri_wkt = 'Longitude_Of_Center'

    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return '+lonc=%s' % self.value

    def to_ogc_wkt(self):
        return 'PARAMETER["Longitude_Of_Center", %s]' % self.value

    def to_esri_wkt(self):
        return 'PARAMETER["Longitude_Of_Center", %s]' % self.value
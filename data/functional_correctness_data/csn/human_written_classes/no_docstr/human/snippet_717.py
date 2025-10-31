class TiltAngle:
    proj4 = '+tilt'

    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return '+tilt=%s' % self.value

    def to_ogc_wkt(self):
        raise Exception('Parameter not supported by OGC WKT')

    def to_esri_wkt(self):
        raise Exception('Parameter not supported by ESRI WKT')
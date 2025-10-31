class DatumShift:
    proj4 = '+towgs84'
    ogc_wkt = 'TOWGS84'

    def __init__(self, value):
        """
        The WGS84 Datum shift parameter.

        Args:

        - **value**: A list of 3 or 7 term datum transform parameters.
        """
        self.value = value

    def to_proj4(self):
        return '+towgs84=%s' % ','.join((str(val) for val in self.value))

    def to_ogc_wkt(self):
        return 'TOWGS84[%s]' % ','.join((str(val) for val in self.value))

    def to_esri_wkt(self):
        raise Exception('Parameter %r not supported by ESRI WKT' % self)
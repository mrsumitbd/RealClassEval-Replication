class Projection:
    proj4 = '+proj'
    ogc_wkt = 'PROJECTION'
    esri_wkt = 'PROJECTION'
    name = None

    def __init__(self, **kwargs):
        """
        A generic container for the specific projection used.

        Args:

        - **name**: A pycrs.projections.ProjName instance with the name given by each supported format. 
        """
        self.name = kwargs.get('name', self.name)

    def to_proj4(self):
        return '+proj=%s' % self.name.proj4

    def to_ogc_wkt(self):
        return 'PROJECTION["%s"]' % self.name.ogc_wkt

    def to_esri_wkt(self):
        return 'PROJECTION["%s"]' % self.name.esri_wkt
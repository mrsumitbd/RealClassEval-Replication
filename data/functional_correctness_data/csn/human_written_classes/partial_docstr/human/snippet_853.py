class Unit:
    ogc_wkt = 'UNIT'
    esri_wkt = 'UNIT'
    unitname = None
    unitmultiplier = None

    def __init__(self, **kwargs):
        """
        Distance unit parameter. 

        Args:

        - **unitname**: A pycrs.elements.units.UnitName instance with the name given by each supported format. 
        - **unitmultiplier**: A pycrs.elements.units.UnitMultiplier instance. 
        """
        self.unitname = kwargs.get('unitname', self.unitname)
        self.unitmultiplier = kwargs.get('unitmultiplier', self.unitmultiplier)

    def to_proj4(self):
        if isinstance(self, Unknown):
            return '+to_meter=%r' % self.unitmultiplier.value
        else:
            return '+units=%s' % self.unitname.proj4

    def to_ogc_wkt(self):
        return 'UNIT["%s", %r]' % (self.unitname.ogc_wkt, self.unitmultiplier.value)

    def to_esri_wkt(self):
        return 'UNIT["%s", %r]' % (self.unitname.esri_wkt, self.unitmultiplier.value)
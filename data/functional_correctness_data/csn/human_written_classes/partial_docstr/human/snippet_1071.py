class LoadDing0:
    """ Class for modelling a load 

    Attributes
    ----------
    id_db : :obj:`int`
        id according to database table
    geo_data : :shapely:`Shapely Point object<points>`
        The geo-spatial point in the coordinate reference
        system with the SRID:4326 or epsg:4326, this
        is the project used by the ellipsoid WGS 84.
    grid : :class:`~.ding0.core.network.GridDing0`
        The MV or LV grid that this Load is to be a part of.
    peak_load : :obj:`float`
        Peak load of the current object
    building_id : :obj:`int`
        refers to OSM oder eGo^n ID, depending on chosen database

    """

    def __init__(self, **kwargs):
        self.id_db = kwargs.get('id_db', None)
        self.geo_data = kwargs.get('geo_data', None)
        self.grid = kwargs.get('grid', None)
        self.peak_load = kwargs.get('peak_load', None)
        self.peak_load_residential = kwargs.get('peak_load_residential', None)
        self.number_households = kwargs.get('number_households', None)
        self.peak_load_cts = kwargs.get('peak_load_cts', None)
        self.peak_load_industrial = kwargs.get('peak_load_industrial', None)
        self.consumption = kwargs.get('consumption', None)
        self.building_id = kwargs.get('building_id', None)
        self.sector = kwargs.get('sector', None)
        self.type = kwargs.get('type', None)

    @property
    def network(self):
        """
        Getter for the overarching :class:`~.ding0.core.network.NetworkDing0`
        object.

        Returns
        -------
        :class:`~.ding0.core.network.NetworkDing0`
        """
        return self.grid.network
    '@property\n    def pypsa_bus_id(self):\n        """\n        Creates a unique identification for the generator\n        to export to pypsa using the id_db of the mv_grid\n        and the current object\n\n        Returns\n        -------\n        :obj:`str`\n        """\n        return \'_\'.join([\'Bus\', \'mvgd\', str(self.grid.grid_district.lv_load_area.mv_grid_district.mv_grid.                id_db), \'lvgd\', str(self.grid.id_db), \'loa\', str(self.id_db)])'
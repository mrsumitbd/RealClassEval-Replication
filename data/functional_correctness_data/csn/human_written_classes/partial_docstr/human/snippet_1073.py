class LVLoadAreaCentreDing0:
    """
    Defines a region centre in Ding0.

    The centres are used in the MV routing as nodes.

    Note
    -----
    Centre is a point within a region's polygon that is located most central 
    (e.g. in a simple region shape like a circle it's the geometric center).

    Parameters
    ----------
    id_db: :obj:`int`
        unique ID in database (=id of associated load area)
    grid: :obj:`int`
        Descr
    geo_data: :shapely:`Shapely Point object<points>`
        The geo-spatial point in the coordinate reference
        system with the SRID:4326 or epsg:4326, this
        is the project used by the ellipsoid WGS 84.
    lv_load_area: :class:`~.ding0.core.network.regions.LVLoadAreaDing0`
        Descr
    """

    def __init__(self, **kwargs):
        self.id_db = kwargs.get('id_db', None)
        self.grid = kwargs.get('grid', None)
        self.geo_data = kwargs.get('geo_data', None)
        self.lv_load_area = kwargs.get('lv_load_area', None)
        self.osm_id_node = kwargs.get('osm_id_node', None)

    @property
    def network(self):
        return self.lv_load_area.network

    @property
    def pypsa_bus_id(self):
        """Todo: Remove
        Returns specific ID for representing bus in pypsa network.

        Returns
        -------
        :obj:`str`:
            Representative of pypsa bus
        """
        return '_'.join(['Bus', 'mvgd', str(self.grid.id_db), 'lac', str(self.id_db)])

    def __repr__(self):
        return '_'.join(['LVLoadAreaCentre', 'mvgd', str(self.grid.id_db), str(self.id_db)])
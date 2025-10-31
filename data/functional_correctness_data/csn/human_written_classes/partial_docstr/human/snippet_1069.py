class CableDistributorDing0:
    """ Cable distributor (connection point) 

    Attributes
    ----------
    id_db : :obj:`int`
        id according to database table
    geo_data : :shapely:`Shapely Point object<points>`
        The geo-spatial point in the coordinate reference
        system with the SRID:4326 or epsg:4326, this
        is the project used by the ellipsoid WGS 84.
    grid : :class:`~.ding0.core.network.grids.MVGridDing0`
        The MV grid that this ring is to be a part of.

    """

    def __init__(self, **kwargs):
        self.id_db = kwargs.get('id_db', None)
        self.geo_data = kwargs.get('geo_data', None)
        self.grid = kwargs.get('grid', None)
        self.helper_component = kwargs.get('helper_component', None)

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
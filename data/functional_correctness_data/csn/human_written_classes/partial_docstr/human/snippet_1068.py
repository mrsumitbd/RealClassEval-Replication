class BranchDing0:
    """
    When a network has a set of connections that don't form into rings but remain
    as open stubs, these are designated as branches. Typically Branches at the
    MV level branch out of Rings.

    Attributes
    ----------
    length : :obj:`float`
        Length of line given in m
    type : :pandas:`pandas.DataFrame<dataframe>`
        Association to pandas Series. DataFrame with attributes of line/cable.
    id_db : :obj:`int`
        id according to database table
    ring : :class:`~.ding0.core.network.RingDing0`
        The associated :class:`~.ding0.core.network.RingDing0` object
    kind : :obj:`str`
        'line' or 'cable'
    connects_aggregated : :obj`bool`
        A boolean True or False to mark if branch is connecting an
        aggregated Load Area or not. Defaults to False.
    circuit_breaker : :class:`:class:`~.ding0.core.network.CircuitBreakerDing0`
        The circuit breaker that opens or closes this Branch.
    critical : :obj:`bool`
        This a designation of if the branch is critical or not,
        defaults to False.

    Note
    -----
    Important: id_db is not set until whole grid is finished (setting at the end).



    ADDED FOR NEW LV GRID APPROACH:
    geometry : shapely.LineString
        due to for lv grids the coordinates of nodes and
        edges are known coordinates are stored as LineString 
        to enable visualisation of the right course of the road.
    """

    def __init__(self, **kwargs):
        self.id_db = kwargs.get('id_db', None)
        self.ring = kwargs.get('ring', None)
        self.feeder = kwargs.get('feeder', None)
        self.grid = kwargs.get('grid', None)
        self.length = kwargs.get('length', None)
        self.kind = kwargs.get('kind', None)
        self.type = kwargs.get('type', None)
        self.connects_aggregated = kwargs.get('connects_aggregated', False)
        self.circuit_breaker = kwargs.get('circuit_breaker', None)
        self.geometry = kwargs.get('geometry', None)
        self.num_parallel = 1
        self.critical = False
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
        return self.ring.network

    def __repr__(self):
        """
        The Representative of the :class:`~.ding0.core.network.BranchDing0` object.

        Returns
        -------
        :obj:`str`
        """
        nodes = sorted(self.grid.graph_nodes_from_branch(self), key=lambda _: repr(_))
        return '_'.join(['Branch', repr(nodes[0]), repr(nodes[1])])
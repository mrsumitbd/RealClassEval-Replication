class NearestQueryResult:
    """
    Stores the nearest points and attributes for nearest points queries.
    """

    def __init__(self):
        self.nearest = None
        self.distances = None
        self.normals = None
        self.triangle_indices = None
        self.barycentric_coordinates = None
        self.interpolated_normals = None
        self.vertex_indices = None

    def has_normals(self):
        return self.normals is not None or self.interpolated_normals is not None
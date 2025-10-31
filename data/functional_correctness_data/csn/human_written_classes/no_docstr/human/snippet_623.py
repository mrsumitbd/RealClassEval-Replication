class MockTracer:

    def __init__(self, traced_grid_2d_list_from=None, image_plane_mesh_grid_pg_list=None):
        self.image_plane_mesh_grid_pg_list = image_plane_mesh_grid_pg_list
        self._traced_grid_2d_list_from = traced_grid_2d_list_from

    def traced_grid_2d_list_from(self, grid):
        return self._traced_grid_2d_list_from

    def plane_index_via_redshift_from(self, redshift):
        raise TypeError
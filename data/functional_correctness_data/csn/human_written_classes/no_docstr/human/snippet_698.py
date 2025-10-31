class Grid:

    def __mul__(self, rgrid):
        return cat_grids(self, rgrid)

    @property
    def nodes(self):
        return self.__nodes__

    @property
    def n_nodes(self):
        return self.__nodes__.shape[0]

    def node(self, i):
        return self.__nodes__[i, :]
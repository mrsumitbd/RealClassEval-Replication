import pandas as pd

class ConnectedComponents:
    """[EXPERIMENTAL] Connected record pairs

    This class identifies connected record pairs. Connected components
    are especially used in detecting duplicates in a single dataset.

    Note
    ----

    This class is experimental and might change in future versions.
    """

    def __init__(self):
        super().__init__()

    def compute(self, links):
        """Return the connected components.

        Parameters
        ----------
        links : pandas.MultiIndex
            The links to apply one-to-one matching on.

        Returns
        -------
        list of pandas.MultiIndex
            A list with pandas.MultiIndex objects. Each MultiIndex
            object represents a set of connected record pairs.

        """
        try:
            import networkx as nx
        except ImportError as err:
            raise Exception("'networkx' module is needed for this operation") from err
        graph_pairs = nx.Graph()
        graph_pairs.add_edges_from(links.values)
        connected_pairs = (graph_pairs.subgraph(c).copy() for c in nx.connected_components(graph_pairs))
        links_result = [pd.MultiIndex.from_tuples(subgraph.edges()) for subgraph in connected_pairs]
        return links_result
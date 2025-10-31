import os
from typing import Union
import networkx as nx
import matplotlib.pyplot as plt


class GraphDisplay:
    '''
    Base class that show processed graph
    '''
    @classmethod
    def _map_edge_color(cls, graph: nx.Graph):
        '''
        Map the graph edge weight to a color.
        Parameters:
        - graph (nxGraph): networkx graph
        Return:
        - List: The list of color code
        '''
        edges = list(graph.edges(data=True))
        if not edges:
            return []
        weights = []
        for _, _, data in edges:
            w = data.get('weight', 1.0)
            try:
                w = float(w)
            except Exception:
                w = 1.0
            weights.append(w)
        wmin = min(weights)
        wmax = max(weights)
        if wmax == wmin:
            norm = [0.5] * len(weights)
        else:
            norm = [(w - wmin) / (wmax - wmin) for w in weights]
        cmap = plt.get_cmap('viridis')
        return [cmap(v) for v in norm]

    @classmethod
    def show_undirected_graph(
        cls,
        graph: Union[str, nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph],
        output_file: str,
        figsize: tuple[float, float] = (36.0, 20.0),
        default_node_sizes: Union[float, int, dict, list, None] = None,
    ):
        '''
        Reads a .graphml file and displays the undirected graph.
        Parameters:
        - graph (str or nx.Graph): graph to be visualized, either a path to a .graphml file
          or a networkx graph instance
        - output_file (str): Path to the output graph image
        '''
        if isinstance(graph, str):
            G = nx.read_graphml(graph)
        else:
            G = graph

        if isinstance(G, (nx.DiGraph, nx.MultiDiGraph)):
            UG = G.to_undirected()
        elif isinstance(G, (nx.Graph, nx.MultiGraph)):
            UG = G.copy()
        else:
            raise TypeError(
                'graph must be a path to .graphml or a networkx graph')

        pos = nx.spring_layout(UG, seed=42)

        if default_node_sizes is None:
            node_sizes = 300
        elif isinstance(default_node_sizes, dict):
            node_sizes = [default_node_sizes.get(n, 300) for n in UG.nodes()]
        else:
            node_sizes = default_node_sizes

        edge_colors = cls._map_edge_color(UG)
        edges_with_data = list(UG.edges(data=True))
        if edges_with_data:
            weights = []
            for _, _, d in edges_with_data:
                w = d.get('weight', 1.0)
                try:
                    w = float(w)
                except Exception:
                    w = 1.0
                weights.append(w)
            wmin = min(weights)
            wmax = max(weights)
            if wmax == wmin:
                widths = [1.5] * len(weights)
            else:
                widths = [1.0 + 3.0 * (w - wmin) / (wmax - wmin)
                          for w in weights]
        else:
            widths = []

        plt.figure(figsize=figsize)
        nx.draw_networkx_nodes(UG, pos, node_size=node_sizes,
                               node_color='#1f78b4', alpha=0.9)
        nx.draw_networkx_edges(
            UG, pos, edge_color=edge_colors, width=widths, alpha=0.8)
        nx.draw_networkx_labels(UG, pos, font_size=10)
        plt.axis('off')
        plt.tight_layout()

        os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
        plt.savefig(output_file, dpi=200, bbox_inches='tight')
        plt.close()

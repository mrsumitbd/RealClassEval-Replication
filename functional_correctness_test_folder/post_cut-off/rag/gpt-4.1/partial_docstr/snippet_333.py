import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.colors import Normalize
from matplotlib import cm


class GraphDisplay:
    '''
    Base class that show processed graph
    '''
    @classmethod
    def _map_edge_color(cls, graph: nx.Graph):
        '''
        Map the graphnode weight to a color.
        Parameters:
        - graph (nxGraph): networkx graph
        Return:
        - List: The list of color code
        '''
        weights = []
        for u, v, data in graph.edges(data=True):
            weight = data.get('weight', 1.0)
            weights.append(weight)
        if not weights:
            return []
        norm = Normalize(vmin=min(weights), vmax=max(weights))
        cmap = cm.get_cmap('viridis')
        colors = [cmap(norm(w)) for w in weights]
        return colors

    @classmethod
    def show_undirected_graph(cls, graph, output_file: str, figsize: tuple[float, float] = (36.0, 20.0), default_node_sizes=300):
        '''
        Reads a .graphml file and displays the undirected graph.
        Parameters:
        - graph (str): graph to be visualized, in networkx.Graph format
        - output_file (str): Path to the output graph image
        '''
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(graph, seed=42)
        edge_colors = cls._map_edge_color(graph)
        node_sizes = []
        for n in graph.nodes():
            size = graph.nodes[n].get('size', default_node_sizes)
            node_sizes.append(size)
        nx.draw_networkx_nodes(graph, pos, node_size=node_sizes)
        nx.draw_networkx_edges(graph, pos, edge_color=edge_colors, width=2)
        nx.draw_networkx_labels(graph, pos)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()

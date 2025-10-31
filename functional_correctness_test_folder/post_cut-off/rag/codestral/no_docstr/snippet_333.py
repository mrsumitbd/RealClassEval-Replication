
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from typing import List


class GraphDisplay:
    '''
    Base class that show processed graph
    '''
    @classmethod
    def _map_edge_color(cls, graph: nx.Graph) -> List[str]:
        '''
        Map the graphnode weight to a color.
        Parameters:
        - graph (nxGraph): networkx graph
        Return:
        - List: The list of color code
        '''
        edge_weights = [graph[u][v].get('weight', 1) for u, v in graph.edges()]
        if not edge_weights:
            return ['black'] * len(graph.edges())

        norm = mcolors.Normalize(
            vmin=min(edge_weights), vmax=max(edge_weights))
        cmap = plt.cm.viridis
        edge_colors = [mcolors.rgb2hex(cmap(norm(w))) for w in edge_weights]
        return edge_colors

    @classmethod
    def show_undirected_graph(cls, graph: nx.Graph, output_file: str, figsize: tuple[float, float] = (36.0, 20.0), default_node_size: int = 300):
        '''
        Reads a .graphml file and displays the undirected graph.
        Parameters:
        - graph (str): graph to be visualized, in networkx.Graph format
        - output_file (str): Path to the output graph image
        '''
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(graph)

        node_colors = ['skyblue'] * len(graph.nodes())
        edge_colors = cls._map_edge_color(graph)

        nx.draw_networkx_nodes(
            graph, pos, node_size=default_node_size, node_color=node_colors)
        nx.draw_networkx_edges(graph, pos, edge_color=edge_colors, width=2)
        nx.draw_networkx_labels(graph, pos, font_size=10,
                                font_family='sans-serif')

        plt.axis('off')
        plt.savefig(output_file, bbox_inches='tight', dpi=300)
        plt.close()

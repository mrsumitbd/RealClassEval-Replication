
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Tuple


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
        colors = []
        for u, v, data in graph.edges(data=True):
            weight = data.get('weight', 1.0)
            # Normalize weight to [0, 1] and map to a colormap (e.g., 'viridis')
            normalized_weight = (weight - min(d.get('weight', 1.0) for _, _, d in graph.edges(data=True))) / \
                (max(d.get('weight', 1.0) for _, _, d in graph.edges(data=True)) -
                 min(d.get('weight', 1.0) for _, _, d in graph.edges(data=True)) + 1e-9)
            # Use a colormap to get the color
            cmap = plt.cm.viridis
            colors.append(cmap(normalized_weight))
        return colors

    @classmethod
    def show_undirected_graph(cls, graph: nx.Graph, output_file: str,
                              figsize: Tuple[float, float] = (36.0, 20.0),
                              default_node_size: int = 300) -> None:
        '''
        Reads a .graphml file and displays the undirected graph.
        Parameters:
        - graph (str): graph to be visualized, in networkx.Graph format
        - output_file (str): Path to the output graph image
        - figsize (tuple[float, float]): Figure size (width, height)
        - default_node_size (int): Default node size
        '''
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(graph, k=0.15, iterations=20)

        # Draw nodes
        nx.draw_networkx_nodes(
            graph, pos, node_size=default_node_size, node_color='skyblue')

        # Draw edges with mapped colors
        edge_colors = cls._map_edge_color(graph)
        nx.draw_networkx_edges(graph, pos, edge_color=edge_colors, width=1.0)

        # Draw labels
        nx.draw_networkx_labels(graph, pos, font_size=8,
                                font_family='sans-serif')

        plt.axis('off')
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()


import networkx as nx
import matplotlib.pyplot as plt
from typing import Tuple, List


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
        edge_colors = []
        for u, v, data in graph.edges(data=True):
            if 'weight' in data:
                # Map weight to a color gradient (example: from light to dark blue)
                weight = data['weight']
                normalized_weight = (weight - min(data['weight'] for _, _, data in graph.edges(data=True))) / \
                    (max(data['weight'] for _, _, data in graph.edges(data=True)) -
                     min(data['weight'] for _, _, data in graph.edges(data=True)) + 1e-10)
                # Dark blue to lighter blue
                edge_colors.append((0.0, 0.0, 0.5 + 0.5 * normalized_weight))
            else:
                # Default color if no weight is present
                edge_colors.append('gray')
        return edge_colors

    @classmethod
    def show_undirected_graph(cls, graph: nx.Graph, output_file: str,
                              figsize: Tuple[float, float] = (36.0, 20.0),
                              default_node_size: int = 300) -> None:
        '''
        Reads a .graphml file and displays the undirected graph.
        Parameters:
        - graph (nx.Graph): graph to be visualized, in networkx.Graph format
        - output_file (str): Path to the output graph image
        - figsize (tuple): Figure size (width, height)
        - default_node_size (int): Default node size for visualization
        '''
        plt.figure(figsize=figsize)
        # Consistent layout for reproducibility
        pos = nx.spring_layout(graph, seed=42)

        # Draw nodes
        nx.draw_networkx_nodes(
            graph, pos, node_size=default_node_size, node_color='skyblue')

        # Draw edges with mapped colors
        edge_colors = cls._map_edge_color(graph)
        nx.draw_networkx_edges(graph, pos, edge_color=edge_colors, width=2.0)

        # Draw labels
        nx.draw_networkx_labels(graph, pos, font_size=10,
                                font_family='sans-serif')

        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file, format='png', dpi=300, bbox_inches='tight')
        plt.close()

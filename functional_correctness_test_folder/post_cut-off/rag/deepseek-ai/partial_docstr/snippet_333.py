
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
        edge_colors = []
        for u, v, data in graph.edges(data=True):
            if 'weight' in data:
                weight = data['weight']
                # Normalize weight to a color (example: grayscale)
                color_intensity = min(1.0, max(0.0, weight))
                edge_colors.append(
                    f'#{int(color_intensity * 255):02x}{int(color_intensity * 255):02x}{int(color_intensity * 255):02x}')
            else:
                edge_colors.append('#000000')  # Default black
        return edge_colors

    @classmethod
    def show_undirected_graph(cls, graph: nx.Graph, output_file: str, figsize: Tuple[float, float] = (36.0, 20.0), default_node_size: int = 300) -> None:
        '''
        Reads a .graphml file and displays the undirected graph.
        Parameters:
        - graph (nxGraph): graph to be visualized, in networkx.Graph format
        - output_file (str): Path to the output graph image
        - figsize (tuple): Figure size (width, height)
        - default_node_size (int): Default node size for visualization
        '''
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(graph)  # or other layout algorithms
        edge_colors = cls._map_edge_color(graph)

        nx.draw_networkx_nodes(graph, pos, node_size=default_node_size)
        nx.draw_networkx_edges(graph, pos, edge_color=edge_colors)
        nx.draw_networkx_labels(graph, pos)

        plt.axis('off')
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()

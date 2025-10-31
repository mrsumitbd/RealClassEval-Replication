
import networkx as nx
import matplotlib.pyplot as plt
from typing import Tuple


class GraphDisplay:
    '''
    Base class that show processed graph
    '''
    @classmethod
    def _map_edge_color(cls, graph: nx.Graph):
        edge_colors = []
        for u, v, data in graph.edges(data=True):
            if 'color' in data:
                edge_colors.append(data['color'])
            else:
                edge_colors.append('black')  # default color
        return edge_colors

    @classmethod
    def show_undirected_graph(cls, graph, output_file: str, figsize: Tuple[float, float] = (36.0, 20.0), default_node_size: int = 500):
        '''
        Reads a .graphml file and displays the undirected graph.
        Parameters:
        - graph (str): graph to be visualized, in networkx.Graph format
        - output_file (str): Path to the output graph image
        - figsize (tuple[float, float]): Figure size (width, height)
        - default_node_size (int): Default node size if not specified in the graph
        '''
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(graph)

        # Node attributes
        node_colors = [data.get('color', 'skyblue')
                       for _, data in graph.nodes(data=True)]
        node_sizes = [data.get('size', default_node_size)
                      for _, data in graph.nodes(data=True)]

        # Edge attributes
        edge_colors = cls._map_edge_color(graph)
        edge_widths = [data.get('width', 1.0)
                       for _, _, data in graph.edges(data=True)]

        nx.draw_networkx_nodes(
            graph, pos, node_color=node_colors, node_size=node_sizes)
        nx.draw_networkx_edges(
            graph, pos, edge_color=edge_colors, width=edge_widths)
        nx.draw_networkx_labels(graph, pos)

        plt.axis('off')
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()

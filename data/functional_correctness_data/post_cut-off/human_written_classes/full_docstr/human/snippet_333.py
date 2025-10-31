import networkx as nx
from matplotlib import colormaps as cm
import matplotlib.pyplot as plt
from typing import List, Union
import numpy as np

class GraphDisplay:
    """
    Base class that show processed graph
    """

    @classmethod
    def _map_edge_color(cls, graph: nx.Graph):
        """
        Map the graphnode weight to a color.

        Parameters:
        - graph (nxGraph): networkx graph

        Return:
        - List: The list of color code
        """
        edge_weights: List[Union[int, float]] = [data.get('weight', 1.0) for _, _, data in graph.edges(data=True)]
        weights_array = np.array(edge_weights, dtype=float)
        min_w = weights_array.min()
        max_w = weights_array.max()
        if max_w > min_w:
            norm_weights = (weights_array - min_w) / (max_w - min_w)
        else:
            norm_weights = weights_array / max_w
        cmap = cm.get_cmap('viridis')
        edge_colors = [cmap(w) for w in norm_weights]
        return edge_colors

    @classmethod
    def show_undirected_graph(cls, graph, output_file: str, figsize: tuple[float, float]=(36.0, 20.0), default_node_sizes: int=500, fig_format: str='svg', dpi: int=300, font_size: int=10, scale_factor: int=20) -> bool:
        """
        Reads a .graphml file and displays the undirected graph.

        Parameters:
        - graph (str): graph to be visualized, in networkx.Graph format
        - output_file (str): Path to the output graph image
        """
        try:
            node_sizes = {}
            node_colors = []
            node_labels = {}
            if graph.is_directed():
                graph = graph.to_undirected()
            communities = nx.get_node_attributes(graph, 'community')
            if communities:
                unique_communities = set(communities.values())
                community_color_map = {community: i for i, community in enumerate(unique_communities)}
                node_colors = [community_color_map[communities[node]] for node in graph.nodes()]
            node_labels = {str(node): str(node) for node in graph.nodes()}
            node_sizes = nx.get_node_attributes(graph, 'node_size')
            if not node_sizes:
                node_sizes = default_node_sizes
            else:
                node_sizes = [node_sizes[node] * scale_factor for node in graph.nodes()]
            if not node_colors:
                node_colors = 'lightblue'
            edge_colors = cls._map_edge_color(graph)
            plt.figure(figsize=figsize)
            pos = nx.spring_layout(graph, seed=42)
            nx.draw(graph, pos, with_labels=True, labels=node_labels, node_color=node_colors, cmap=plt.get_cmap('rainbow'), node_size=node_sizes, font_size=font_size, edge_color=edge_colors)
            plt.title('Graph with Communities')
            plt.savefig(output_file, format=fig_format, dpi=dpi)
            plt.clf()
            plt.close()
            logger.info('Graph saved to %s', output_file)
        except nx.NetworkXError as e:
            logger.error('Networkx graph file error %s', str(e))
            return False
        except Exception as e:
            logger.error('An error occurred during graph display: %s', str(e))
            return False
        return True
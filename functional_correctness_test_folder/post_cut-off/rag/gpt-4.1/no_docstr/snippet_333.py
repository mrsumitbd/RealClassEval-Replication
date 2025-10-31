import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np


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
        # Get edge weights
        weights = []
        for u, v, data in graph.edges(data=True):
            weight = data.get('weight', 1.0)
            weights.append(weight)
        if not weights:
            return []
        weights = np.array(weights)
        # Normalize weights to [0,1]
        min_w = weights.min()
        max_w = weights.max()
        if max_w == min_w:
            norm_weights = np.ones_like(weights) * 0.5
        else:
            norm_weights = (weights - min_w) / (max_w - min_w)
        # Map to colormap
        cmap = cm.get_cmap('viridis')
        colors = [cmap(w) for w in norm_weights]
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
        # Node sizes
        if isinstance(default_node_sizes, dict):
            node_sizes = [default_node_sizes.get(
                n, 300) for n in graph.nodes()]
        else:
            node_sizes = default_node_sizes
        # Node colors
        node_colors = [graph.nodes[n].get(
            'color', '#1f78b4') for n in graph.nodes()]
        # Edge colors
        edge_colors = cls._map_edge_color(graph)
        # Draw
        nx.draw_networkx_nodes(
            graph, pos, node_size=node_sizes, node_color=node_colors)
        nx.draw_networkx_edges(
            graph, pos, edge_color=edge_colors if edge_colors else '#888', width=2)
        nx.draw_networkx_labels(graph, pos, font_size=12)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()

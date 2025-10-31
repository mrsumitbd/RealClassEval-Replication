
import networkx as nx
import matplotlib.pyplot as plt


class GraphDisplay:
    '''
    Base class that show processed graph
    '''
    @classmethod
    def _map_edge_color(cls, graph: nx.Graph):
        '''
        Map the graph node weight to a color.
        Parameters:
        - graph (nx.Graph): networkx graph
        Return:
        - List: The list of color code
        '''
        edge_weights = [graph[u][v].get('weight', 1) for u, v in graph.edges()]
        max_weight = max(edge_weights)
        min_weight = min(edge_weights)
        return [(weight - min_weight) / (max_weight - min_weight) if max_weight != min_weight else 0.5 for weight in edge_weights]

    @classmethod
    def show_undirected_graph(cls, graph: nx.Graph, output_file: str, figsize: tuple[float, float] = (36.0, 20.0), default_node_size: float = 100.0):
        '''
        Displays the undirected graph.
        Parameters:
        - graph (nx.Graph): graph to be visualized, in networkx.Graph format
        - output_file (str): Path to the output graph image
        - figsize (tuple[float, float]): Figure size for the plot. Defaults to (36.0, 20.0).
        - default_node_size (float): Default size for the nodes. Defaults to 100.0.
        '''
        pos = nx.spring_layout(graph)
        edge_colors = cls._map_edge_color(graph)
        plt.figure(figsize=figsize)
        nx.draw_networkx_nodes(graph, pos, node_size=default_node_size)
        nx.draw_networkx_labels(graph, pos)
        nx.draw_networkx_edges(
            graph, pos, edge_color=edge_colors, edge_cmap=plt.cm.Blues)
        plt.axis('off')
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()


import networkx as nx
import matplotlib.pyplot as plt


class GraphDisplay:
    '''
    Base class that show processed graph
    '''
    @classmethod
    def _map_edge_color(cls, graph: nx.Graph):
        edge_colors = ['blue' if graph[u][v]['weight']
                       >= 0 else 'red' for u, v in graph.edges()]
        return edge_colors

    @classmethod
    def show_undirected_graph(cls, graph: nx.Graph, output_file: str, figsize: tuple[float, float] = (36.0, 20.0), default_node_size: float = 100.0):
        '''
        Displays the undirected graph.
        Parameters:
        - graph (nx.Graph): graph to be visualized, in networkx.Graph format
        - output_file (str): Path to the output graph image
        - figsize (tuple[float, float]): Size of the output figure. Defaults to (36.0, 20.0).
        - default_node_size (float): Size of the nodes. Defaults to 100.0.
        '''
        pos = nx.spring_layout(graph)
        edge_colors = cls._map_edge_color(graph)
        plt.figure(figsize=figsize)
        nx.draw_networkx(graph, pos, node_size=default_node_size,
                         edge_color=edge_colors)
        plt.savefig(output_file)
        plt.close()

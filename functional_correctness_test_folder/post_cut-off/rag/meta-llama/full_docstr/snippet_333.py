
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
        edge_colors = []
        for _, _, data in graph.edges(data=True):
            if 'weight' in data:
                edge_colors.append(data['weight'])
            else:
                edge_colors.append(1.0)  # default weight
        return edge_colors

    @classmethod
    def show_undirected_graph(cls, graph: nx.Graph, output_file: str, figsize: tuple[float, float] = (36.0, 20.0), default_node_size: float = 300.0):
        '''
        Displays the undirected graph.

        Parameters:
        - graph (nx.Graph): graph to be visualized, in networkx.Graph format
        - output_file (str): Path to the output graph image
        - figsize (tuple[float, float]): Figure size for the plot. Defaults to (36.0, 20.0)
        - default_node_size (float): Default node size. Defaults to 300.0
        '''
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(graph)
        edge_colors = cls._map_edge_color(graph)
        nx.draw_networkx_nodes(graph, pos, node_size=default_node_size)
        nx.draw_networkx_labels(graph, pos)
        nx.draw_networkx_edges(
            graph, pos, edge_color=edge_colors, edge_cmap=plt.cm.Reds)
        edge_labels = {(u, v): d.get('weight', '')
                       for u, v, d in graph.edges(data=True)}
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
        plt.axis('off')
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()

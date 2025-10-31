
import networkx as nx
import matplotlib.pyplot as plt


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
                edge_colors.append('black')
        return edge_colors

    @classmethod
    def show_undirected_graph(cls, graph, output_file: str, figsize: tuple[float, float] = (36.0, 20.0), default_node_sizes=1000):
        '''
        Reads a .graphml file and displays the undirected graph.
        Parameters:
        - graph (str): graph to be visualized, in networkx.Graph format
        - output_file (str): Path to the output graph image
        '''
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(graph)
        edge_colors = cls._map_edge_color(graph)
        nx.draw(graph, pos, with_labels=True,
                node_size=default_node_sizes, edge_color=edge_colors)
        plt.savefig(output_file)
        plt.close()


import networkx as nx
import matplotlib.pyplot as plt


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
        edge_colors = []
        for u, v, data in graph.edges(data=True):
            if 'weight' in data:
                edge_colors.append(data['weight'])
            else:
                edge_colors.append(1.0)
        return edge_colors

    @classmethod
    def show_undirected_graph(cls, graph, output_file: str, figsize: tuple[float, float] = (36.0, 20.0), default_node_size=300):
        '''
        Reads a .graphml file and displays the undirected graph.
        Parameters:
        - graph (str): graph to be visualized, in networkx.Graph format
        - output_file (str): Path to the output graph image
        '''
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(graph)
        edge_colors = cls._map_edge_color(graph)
        nx.draw(graph, pos, with_labels=True, node_size=default_node_size,
                edge_color=edge_colors, edge_cmap=plt.cm.Blues, width=2)
        plt.savefig(output_file)
        plt.close()

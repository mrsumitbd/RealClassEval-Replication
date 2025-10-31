
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class GraphDisplay:
    '''
    Base class that show processed graph
    '''
    @classmethod
    def _map_edge_color(cls, graph: nx.Graph):
        '''
        Map the graphnode weight to a color.
        Parameters:
        - graph (nx.Graph): networkx graph
        Return:
        - List: The list of color code
        '''
        weights = nx.get_edge_attributes(graph, 'weight')
        if not weights:
            return ['black'] * len(graph.edges())
        max_weight = max(weights.values())
        min_weight = min(weights.values())
        norm = mcolors.Normalize(vmin=min_weight, vmax=max_weight)
        cmap = plt.cm.get_cmap('coolwarm')
        return [cmap(norm(weight)) for weight in weights.values()]

    @classmethod
    def show_undirected_graph(cls, graph, output_file: str, figsize: tuple[float, float] = (36.0, 20.0), default_node_size: int = 300):
        '''
        Reads a .graphml file and displays the undirected graph.
        Parameters:
        - graph (nx.Graph): graph to be visualized, in networkx.Graph format
        - output_file (str): Path to the output graph image
        - figsize (tuple[float, float]): Size of the figure
        - default_node_size (int): Default size of the nodes
        '''
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(graph, seed=42)
        edge_colors = cls._map_edge_color(graph)
        nx.draw_networkx_nodes(graph, pos, node_size=default_node_size)
        nx.draw_networkx_edges(graph, pos, edge_color=edge_colors)
        nx.draw_networkx_labels(graph, pos, font_size=10,
                                font_family="sans-serif")
        plt.axis('off')
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()

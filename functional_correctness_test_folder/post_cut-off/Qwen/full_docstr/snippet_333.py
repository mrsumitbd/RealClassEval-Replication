
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
        - graph (nxGraph): networkx graph
        Return:
        - List: The list of color code
        '''
        weights = [graph[u][v].get('weight', 1) for u, v in graph.edges()]
        norm = mcolors.Normalize(vmin=min(weights), vmax=max(weights))
        cmap = plt.cm.get_cmap('coolwarm')
        return [cmap(norm(weight)) for weight in weights]

    @classmethod
    def show_undirected_graph(cls, graph, output_file: str, figsize: tuple[float, float] = (36.0, 20.0), default_node_size: int = 300):
        '''
        Reads a .graphml file and displays the undirected graph.
        Parameters:
        - graph (str): graph to be visualized, in networkx.Graph format
        - output_file (str): Path to the output graph image
        '''
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(graph, seed=42)
        edge_colors = cls._map_edge_color(graph)
        nx.draw_networkx_nodes(graph, pos, node_size=default_node_size)
        nx.draw_networkx_edges(graph, pos, edge_color=edge_colors)
        nx.draw_networkx_labels(graph, pos, font_size=10,
                                font_family="sans-serif")
        plt.colorbar(plt.cm.ScalarMappable(norm=mcolors.Normalize(
            vmin=min(edge_colors), vmax=max(edge_colors)), cmap='coolwarm'), ax=plt.gca())
        plt.axis('off')
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()


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
        Map the graph edge weight to a color.
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
            return ['#1f78b4'] * graph.number_of_edges()
        min_w = min(weights)
        max_w = max(weights)
        norm = mcolors.Normalize(vmin=min_w, vmax=max_w)
        cmap = plt.get_cmap('coolwarm')
        colors = [cmap(norm(w)) for w in weights]
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
        node_sizes = []
        for n in graph.nodes(data=True):
            size = n[1].get('size', default_node_sizes)
            node_sizes.append(size)
        node_colors = []
        for n in graph.nodes(data=True):
            color = n[1].get('color', '#1f78b4')
            node_colors.append(color)
        edge_colors = cls._map_edge_color(graph)
        nx.draw_networkx_nodes(
            graph, pos, node_size=node_sizes, node_color=node_colors)
        nx.draw_networkx_edges(graph, pos, edge_color=edge_colors, width=2)
        nx.draw_networkx_labels(graph, pos, font_size=10)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()

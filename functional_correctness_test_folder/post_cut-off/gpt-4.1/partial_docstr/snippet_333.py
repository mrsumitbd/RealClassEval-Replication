
import networkx as nx
import matplotlib.pyplot as plt


class GraphDisplay:
    '''
    Base class that show processed graph
    '''
    @classmethod
    def _map_edge_color(cls, graph: nx.Graph):
        # Map edge color based on 'color' attribute, default to 'black'
        edge_colors = []
        for u, v, data in graph.edges(data=True):
            color = data.get('color', 'black')
            edge_colors.append(color)
        return edge_colors

    @classmethod
    def show_undirected_graph(
        cls,
        graph,
        output_file: str,
        figsize: tuple[float, float] = (36.0, 20.0),
        default_node_sizes=300
    ):
        '''
        Reads a .graphml file and displays the undirected graph.
        Parameters:
        - graph (str): graph to be visualized, in networkx.Graph format
        - output_file (str): Path to the output graph image
        '''
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(graph, seed=42)

        # Node colors
        node_colors = []
        for n, data in graph.nodes(data=True):
            color = data.get('color', 'skyblue')
            node_colors.append(color)

        # Node sizes
        if isinstance(default_node_sizes, dict):
            node_sizes = [default_node_sizes.get(
                n, 300) for n in graph.nodes()]
        else:
            node_sizes = [default_node_sizes for _ in graph.nodes()]

        # Edge colors
        edge_colors = cls._map_edge_color(graph)

        nx.draw_networkx_nodes(
            graph, pos,
            node_color=node_colors,
            node_size=node_sizes,
            alpha=0.9
        )
        nx.draw_networkx_edges(
            graph, pos,
            edge_color=edge_colors,
            width=2,
            alpha=0.7
        )
        nx.draw_networkx_labels(graph, pos, font_size=12, font_color='black')

        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file, format='png')
        plt.close()


import networkx as nx
import matplotlib.pyplot as plt


class GraphDisplay:

    @classmethod
    def _map_edge_color(cls, graph: nx.Graph):
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
        default_node_sizes: int = 300
    ):
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(graph)
        node_colors = [data.get('color', 'skyblue')
                       for _, data in graph.nodes(data=True)]
        node_sizes = [data.get('size', default_node_sizes)
                      for _, data in graph.nodes(data=True)]
        edge_colors = cls._map_edge_color(graph)
        nx.draw_networkx_nodes(
            graph, pos, node_color=node_colors, node_size=node_sizes)
        nx.draw_networkx_edges(graph, pos, edge_color=edge_colors)
        nx.draw_networkx_labels(graph, pos)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()

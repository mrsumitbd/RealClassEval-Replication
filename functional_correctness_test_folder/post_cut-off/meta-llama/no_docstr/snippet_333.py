
import networkx as nx
import matplotlib.pyplot as plt


class GraphDisplay:

    @classmethod
    def _map_edge_color(cls, graph: nx.Graph):
        edge_colors = []
        for u, v in graph.edges():
            if graph[u][v].get('color') is not None:
                edge_colors.append(graph[u][v]['color'])
            else:
                edge_colors.append('black')
        return edge_colors

    @classmethod
    def show_undirected_graph(cls, graph: nx.Graph, output_file: str, figsize: tuple[float, float] = (36.0, 20.0), default_node_size: float = 300.0):
        pos = nx.spring_layout(graph)
        node_sizes = [graph.nodes[node].get(
            'size', default_node_size) for node in graph.nodes()]
        edge_colors = cls._map_edge_color(graph)
        plt.figure(figsize=figsize)
        nx.draw_networkx(graph, pos, node_size=node_sizes,
                         edge_color=edge_colors)
        plt.savefig(output_file)
        plt.close()

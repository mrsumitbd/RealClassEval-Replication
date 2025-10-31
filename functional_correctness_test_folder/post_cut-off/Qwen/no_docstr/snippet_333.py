
import networkx as nx
import matplotlib.pyplot as plt


class GraphDisplay:

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
    def show_undirected_graph(cls, graph, output_file: str, figsize: tuple[float, float] = (36.0, 20.0), default_node_size: int = 300):
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(graph)
        node_sizes = [graph.nodes[node].get(
            'size', default_node_size) for node in graph.nodes()]
        edge_colors = cls._map_edge_color(graph)
        nx.draw(graph, pos, with_labels=True, node_size=node_sizes,
                edge_color=edge_colors, node_color='skyblue', font_size=10, font_weight='bold')
        plt.savefig(output_file)
        plt.close()

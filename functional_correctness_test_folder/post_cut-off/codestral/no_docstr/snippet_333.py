
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
    def show_undirected_graph(cls, graph, output_file: str, figsize: tuple[float, float] = (36.0, 20.0), default_node_size=300):
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(graph)
        node_colors = [graph.nodes[n].get(
            'color', 'skyblue') for n in graph.nodes()]
        edge_colors = cls._map_edge_color(graph)
        nx.draw_networkx_nodes(
            graph, pos, node_size=default_node_size, node_color=node_colors)
        nx.draw_networkx_edges(graph, pos, edge_color=edge_colors)
        nx.draw_networkx_labels(graph, pos)
        plt.axis('off')
        plt.savefig(output_file, format="PNG")
        plt.close()

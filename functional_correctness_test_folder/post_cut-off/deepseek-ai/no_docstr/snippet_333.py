
import networkx as nx
import matplotlib.pyplot as plt
from typing import Optional, Dict, Any


class GraphDisplay:

    @classmethod
    def _map_edge_color(cls, graph: nx.Graph) -> list:
        edge_colors = []
        for u, v, data in graph.edges(data=True):
            if 'color' in data:
                edge_colors.append(data['color'])
            else:
                edge_colors.append('black')
        return edge_colors

    @classmethod
    def show_undirected_graph(
        cls,
        graph: nx.Graph,
        output_file: str,
        figsize: tuple[float, float] = (36.0, 20.0),
        default_node_size: int = 300,
        node_size_map: Optional[Dict[Any, int]] = None,
        default_node_color: str = 'skyblue',
        node_color_map: Optional[Dict[Any, str]] = None,
        with_labels: bool = True,
        font_size: int = 10,
        font_color: str = 'black',
        edge_width: float = 1.0,
        alpha: float = 1.0
    ) -> None:
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(graph)

        node_sizes = [node_size_map.get(node, default_node_size) for node in graph.nodes(
        )] if node_size_map else [default_node_size] * len(graph.nodes())
        node_colors = [node_color_map.get(node, default_node_color) for node in graph.nodes(
        )] if node_color_map else [default_node_color] * len(graph.nodes())
        edge_colors = cls._map_edge_color(graph)

        nx.draw_networkx_nodes(
            graph,
            pos,
            node_size=node_sizes,
            node_color=node_colors,
            alpha=alpha
        )

        nx.draw_networkx_edges(
            graph,
            pos,
            width=edge_width,
            edge_color=edge_colors,
            alpha=alpha
        )

        if with_labels:
            nx.draw_networkx_labels(
                graph,
                pos,
                font_size=font_size,
                font_color=font_color
            )

        plt.axis('off')
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()

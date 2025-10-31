
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import networkx as nx
from typing import List, Tuple, Union


class GraphDisplay:
    """
    Base class that shows processed graphs.
    """

    @classmethod
    def _map_edge_color(cls, graph: nx.Graph) -> List[str]:
        """
        Map the edge weight to a color.

        Parameters
        ----------
        graph : nx.Graph
            NetworkX graph whose edges have a ``weight`` attribute.

        Returns
        -------
        List[str]
            List of hex color codes, one per edge, ordered as in ``graph.edges()``.
        """
        # Extract edge weights; default to 1 if missing
        weights = [
            graph[u][v].get("weight", 1.0) for u, v in graph.edges()
        ]

        # Normalise weights to [0, 1] for colormap mapping
        min_w, max_w = min(weights), max(weights)
        if min_w == max_w:
            # Avoid division by zero – all edges same weight
            norm = [0.5] * len(weights)
        else:
            norm = [(w - min_w) / (max_w - min_w) for w in weights]

        # Use a matplotlib colormap to convert normalised values to colors
        cmap = cm.get_cmap("viridis")
        colors = [cmap(n) for n in norm]

        # Convert RGBA tuples to hex strings
        hex_colors = [plt.colors.to_hex(c) for c in colors]
        return hex_colors

    @classmethod
    def show_undirected_graph(
        cls,
        graph: nx.Graph,
        output_file: str,
        figsize: Tuple[float, float] = (36.0, 20.0),
        default_node_sizes: Union[int, List[int]] = 300,
    ) -> None:
        """
        Reads a NetworkX graph and displays the undirected graph.

        Parameters
        ----------
        graph : nx.Graph
            The graph to be visualized.
        output_file : str
            Path to the output graph image (e.g. ``'graph.png'``).
        figsize : tuple[float, float], optional
            Figure size in inches. Default is (36.0, 20.0).
        default_node_sizes : int or list[int], optional
            Size(s) of the nodes. If an int is supplied, all nodes use that size.
            If a list is supplied, it must match ``len(graph.nodes())``.
        """
        # Compute node colors based on node weight if present
        node_weights = [
            graph.nodes[n].get("weight", 1.0) for n in graph.nodes()
        ]
        min_w, max_w = min(node_weights), max(node_weights)
        if min_w == max_w:
            norm = [0.5] * len(node_weights)
        else:
            norm = [(w - min_w) / (max_w - min_w) for w in node_weights]
        cmap = cm.get_cmap("plasma")
        node_colors = [cmap(n) for n in norm]
        node_colors_hex = [plt.colors.to_hex(c) for c in node_colors]

        # Edge colors
        edge_colors = cls._map_edge_color(graph)

        # Node sizes
        if isinstance(default_node_sizes, int):
            node_sizes = [default_node_sizes] * len(graph.nodes())
        else:
            node_sizes = default_node_sizes

        # Layout
        pos = nx.spring_layout(graph, seed=42)

        # Plot
        plt.figure(figsize=figsize)
        nx.draw_networkx(
            graph,
            pos,
            node_color=node_colors_hex,
            edge_color=edge_colors,
            node_size=node_sizes,
            with_labels=True,
            font_color="black",
            font_weight="bold",
        )
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(output_file, dpi=300)
        plt.close()


import os
from pathlib import Path
from typing import Iterable, List, Tuple, Union

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import cm, colors


class GraphDisplay:
    """
    Base class that shows processed graphs.
    """

    @classmethod
    def _map_edge_color(
        cls, graph: nx.Graph
    ) -> List[Union[str, Tuple[float, float, float, float]]]:
        """
        Map the graph node weight to a color for each edge.

        Parameters
        ----------
        graph : nx.Graph
            NetworkX graph whose nodes may have a ``weight`` attribute.

        Returns
        -------
        List
            A list of color codes (hex strings or RGBA tuples) – one per edge.
        """
        # Gather all node weights; default to 0 if missing
        weights = [graph.nodes[n].get("weight", 0) for n in graph.nodes]
        if not weights:
            # No weights – return a default color
            return ["#000000"] * graph.number_of_edges()

        # Normalise weights to [0, 1] for colormap mapping
        min_w, max_w = min(weights), max(weights)
        norm = colors.Normalize(vmin=min_w, vmax=max_w, clip=True)
        cmap = cm.get_cmap("viridis")

        # For each edge, use the average weight of its two endpoints
        edge_colors = []
        for u, v in graph.edges:
            w_u = graph.nodes[u].get("weight", 0)
            w_v = graph.nodes[v].get("weight", 0)
            avg_w = (w_u + w_v) / 2.0
            rgba = cmap(norm(avg_w))
            # Convert RGBA to hex string for matplotlib
            hex_color = colors.to_hex(rgba)
            edge_colors.append(hex_color)

        return edge_colors

    @classmethod
    def show_undirected_graph(
        cls,
        graph: nx.Graph,
        output_file: str,
        figsize: Tuple[float, float] = (36.0, 20.0),
        default_node_sizes: Union[float, dict] = 300,
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
        default_node_sizes : float or dict, optional
            If a float, all nodes will have this size. If a dict, it should map
            node identifiers to sizes. Default is 300.
        """
        # Ensure the graph is undirected
        if graph.is_directed():
            graph = graph.to_undirected()

        # Compute layout
        pos = nx.spring_layout(graph, seed=42)

        # Determine node sizes
        if isinstance(default_node_sizes, dict):
            node_sizes = [default_node_sizes.get(n, 300) for n in graph.nodes]
        else:
            node_sizes = [default_node_sizes] * graph.number_of_nodes()

        # Edge colors
        edge_colors = cls._map_edge_color(graph)

        # Draw
        plt.figure(figsize=figsize)
        nx.draw_networkx_nodes(
            graph,
            pos,
            node_color="lightblue",
            node_size=node_sizes,
            edgecolors="black",
        )
        nx.draw_networkx_edges(
            graph,
            pos,
            edge_color=edge_colors,
            arrows=False,
        )
        nx.draw_networkx_labels(graph, pos, font_size=12, font_color="black")

        plt.axis("off")

        # Ensure output directory exists
        out_path = Path(output_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        # Save figure
        plt.savefig(out_path, format=out_path.suffix[1:], bbox_inches="tight")
        plt.close()

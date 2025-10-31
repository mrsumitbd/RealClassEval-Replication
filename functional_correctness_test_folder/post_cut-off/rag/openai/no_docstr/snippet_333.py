
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import networkx as nx
from typing import Iterable, List, Tuple, Dict, Optional, Union


class GraphDisplay:
    """
    Base class that shows processed graph.
    """

    @classmethod
    def _map_edge_color(
        cls, graph: nx.Graph
    ) -> List[Union[str, Tuple[float, float, float, float]]]:
        """
        Map the graph edge weight to a color.

        Parameters
        ----------
        graph : nx.Graph
            NetworkX graph whose edges have a ``weight`` attribute.

        Returns
        -------
        List
            List of color codes (hex strings or RGBA tuples) corresponding to each edge.
        """
        # Extract weights
        weights: List[float] = []
        for _, _, data in graph.edges(data=True):
            weights.append(float(data.get("weight", 1.0)))

        # If all weights are equal, use a single color
        if len(set(weights)) == 1:
            return ["#1f77b4"] * len(weights)

        # Normalise weights to [0, 1]
        norm = colors.Normalize(vmin=min(weights), vmax=max(weights))
        cmap = cm.get_cmap("viridis")

        # Map each weight to a color
        return [cmap(norm(w)) for w in weights]

    @classmethod
    def show_undirected_graph(
        cls,
        graph: nx.Graph,
        output_file: str,
        figsize: Tuple[float, float] = (36.0, 20.0),
        default_node_sizes: Optional[Dict[Union[int, str], float]] = None,
    ) -> None:
        """
        Visualise an undirected graph and save the figure.

        Parameters
        ----------
        graph : nx.Graph
            NetworkX graph to be visualised.
        output_file : str
            Path to the output image file (e.g. ``'graph.png'``).
        figsize : tuple[float, float], optional
            Size of the figure in inches. Default is (36.0, 20.0).
        default_node_sizes : dict, optional
            Mapping from node to node size. If ``None`` a default size of 300
            is used for all nodes.
        """
        # Compute layout
        try:
            pos = nx.spring_layout(graph, seed=42)
        except Exception:
            pos = nx.random_layout(graph)

        # Node sizes
        if default_node_sizes is None:
            node_sizes = [300] * graph.number_of_nodes()
        else:
            node_sizes = [
                default_node_sizes.get(node, 300) for node in graph.nodes()
            ]

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
        plt.tight_layout()
        plt.savefig(output_file, dpi=300)
        plt.close()

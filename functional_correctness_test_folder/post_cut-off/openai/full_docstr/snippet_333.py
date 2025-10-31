
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from typing import List, Tuple, Optional


class GraphDisplay:
    """
    Base class that shows processed graph.
    """

    @classmethod
    def _map_edge_color(cls, graph: nx.Graph) -> List[str]:
        """
        Map the edge weight to a color.

        Parameters
        ----------
        graph : nx.Graph
            NetworkX graph.

        Returns
        -------
        List[str]
            List of color codes for each edge.
        """
        # Extract edge weights; default to 0 if missing
        weights = []
        for _, _, data in graph.edges(data=True):
            weights.append(data.get("weight", 0))

        # If all weights are equal, use a single color
        if len(set(weights)) <= 1:
            return ["#1f77b4"] * len(weights)

        # Normalize weights to [0, 1]
        norm = mcolors.Normalize(vmin=min(weights), vmax=max(weights))
        cmap = cm.get_cmap("viridis")

        # Map each weight to a color
        colors = [mcolors.to_hex(cmap(norm(w))) for w in weights]
        return colors

    @classmethod
    def show_undirected_graph(
        cls,
        graph: nx.Graph,
        output_file: str,
        figsize: Tuple[float, float] = (36.0, 20.0),
        default_node_sizes: Optional[List[float]] = None,
    ) -> None:
        """
        Display an undirected graph and save it to a file.

        Parameters
        ----------
        graph : nx.Graph
            NetworkX graph to be visualized.
        output_file : str
            Path to the output graph image.
        figsize : Tuple[float, float], optional
            Figure size in inches. Default is (36.0, 20.0).
        default_node_sizes : List[float], optional
            Default node sizes if not specified in node attributes.
        """
        # Compute layout
        pos = nx.spring_layout(graph, seed=42)

        # Node sizes
        if default_node_sizes is None:
            # Try to use node attribute 'size', else default to 300
            node_sizes = []
            for n in graph.nodes():
                size = graph.nodes[n].get("size", 300)
                node_sizes.append(size)
        else:
            node_sizes = default_node_sizes

        # Node colors
        node_colors = []
        for n in graph.nodes():
            color = graph.nodes[n].get("color", "#1f77b4")
            node_colors.append(color)

        # Edge colors
        edge_colors = cls._map_edge_color(graph)

        # Draw graph
        plt.figure(figsize=figsize)
        nx.draw_networkx(
            graph,
            pos,
            node_color=node_colors,
            node_size=node_sizes,
            edge_color=edge_colors,
            with_labels=True,
            font_color="white",
            font_weight="bold",
            edge_cmap=cm.viridis,
        )
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(output_file, dpi=300)
        plt.close()

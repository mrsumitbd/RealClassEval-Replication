
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
from typing import Tuple, Iterable, Union, Optional


class GraphDisplay:
    """
    Utility class for visualising undirected NetworkX graphs.
    """

    @classmethod
    def _map_edge_color(
        cls,
        graph: nx.Graph,
        cmap_name: str = "viridis",
        default_color: str = "gray",
    ) -> list[Union[str, Tuple[float, float, float, float]]]:
        """
        Map edge weights to colors using a matplotlib colormap.

        Parameters
        ----------
        graph : nx.Graph
            The graph whose edges will be coloured.
        cmap_name : str, optional
            Name of the matplotlib colormap to use. Default is 'viridis'.
        default_color : str, optional
            Color to use for edges without a 'weight' attribute. Default is 'gray'.

        Returns
        -------
        list
            A list of colors corresponding to each edge in ``graph.edges``.
        """
        # Extract weights if present
        weights = []
        for u, v, data in graph.edges(data=True):
            w = data.get("weight")
            if w is None:
                weights.append(None)
            else:
                weights.append(w)

        # If all weights are None, return default color for all edges
        if all(w is None for w in weights):
            return [default_color] * len(weights)

        # Determine min/max weight for normalization
        weight_values = [w for w in weights if w is not None]
        vmin, vmax = min(weight_values), max(weight_values)

        # Create colormap and normalization
        cmap = cm.get_cmap(cmap_name)
        norm = colors.Normalize(vmin=vmin, vmax=vmax)

        # Map each weight to a color; use default for missing weights
        edge_colors = []
        for w in weights:
            if w is None:
                edge_colors.append(default_color)
            else:
                edge_colors.append(cmap(norm(w)))

        return edge_colors

    @classmethod
    def show_undirected_graph(
        cls,
        graph: nx.Graph,
        output_file: str,
        figsize: Tuple[float, float] = (36.0, 20.0),
        default_node_sizes: Union[float, Iterable[float]] = 300.0,
        node_color: str = "skyblue",
        edge_color: str = "gray",
        with_labels: bool = True,
        font_size: int = 12,
        title: Optional[str] = None,
        cmap_name: str = "viridis",
    ) -> None:
        """
        Draw an undirected graph and save it to a file.

        Parameters
        ----------
        graph : nx.Graph
            The graph to visualise.
        output_file : str
            Path to the file where the figure will be saved.
        figsize : tuple[float, float], optional
            Size of the figure in inches. Default is (36.0, 20.0).
        default_node_sizes : float or iterable of float, optional
            Size(s) of the nodes. If a single float is provided, all nodes
            will have that size. If an iterable is provided, it must match
            the number of nodes in the graph. Default is 300.0.
        node_color : str, optional
            Color of the nodes. Default is 'skyblue'.
        edge_color : str, optional
            Default color of edges if no weight attribute is present.
            Ignored if edge weights are used. Default is 'gray'.
        with_labels : bool, optional
            Whether to draw node labels. Default is True.
        font_size : int, optional
            Font size for node labels. Default is 12.
        title : str, optional
            Title of the plot. If None, no title is added.
        cmap_name : str, optional
            Colormap to use for edge weights. Default is 'viridis'.

        Returns
        -------
        None
            The figure is saved to ``output_file``.
        """
        # Ensure we are working with an undirected graph
        if graph.is_directed():
            raise ValueError(
                "show_undirected_graph expects an undirected graph.")

        # Compute node sizes
        if isinstance(default_node_sizes, (int, float)):
            node_sizes = [default_node_sizes] * graph.number_of_nodes()
        else:
            node_sizes = list(default_node_sizes)
            if len(node_sizes) != graph.number_of_nodes():
                raise ValueError(
                    "Length of default_node_sizes must match number of nodes in the graph."
                )

        # Map edge colors based on weights if present
        edge_colors = cls._map_edge_color(
            graph, cmap_name=cmap_name, default_color=edge_color)

        # Layout
        pos = nx.spring_layout(graph, seed=42)

        # Create figure
        plt.figure(figsize=figsize)

        # Draw nodes
        nx.draw_networkx_nodes(
            graph,
            pos,
            node_color=node_color,
            node_size=node_sizes,
            edgecolors="black",
            linewidths=0.5,
        )

        # Draw edges
        nx.draw_networkx_edges(
            graph,
            pos,
            edge_color=edge_colors,
            width=1.5,
        )

        # Draw labels
        if with_labels:
            nx.draw_networkx_labels(
                graph,
                pos,
                font_size=font_size,
                font_color="black",
            )

        # Title
        if title:
            plt.title(title, fontsize=font_size + 4)

        # Remove axes
        plt.axis("off")

        # Tight layout
        plt.tight_layout()

        # Save figure
        plt.savefig(output_file, format="png", dpi=300)
        plt.close()

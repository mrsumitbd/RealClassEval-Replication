
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm


class GraphDisplay:
    """
    Base class that show processed graph
    """

    @classmethod
    def _map_edge_color(cls, graph: nx.Graph):
        """
        Map edge colors based on the 'weight' attribute of each edge.
        If an edge has no 'weight', it will be colored gray.
        Returns a list of colors corresponding to the edges in graph.edges().
        """
        # Collect weights
        weights = []
        for u, v, data in graph.edges(data=True):
            weights.append(data.get("weight", None))

        # If all weights are None, return gray for all edges
        if all(w is None for w in weights):
            return ["gray"] * len(weights)

        # Replace None with 0 for colormap mapping
        weights_clean = [w if w is not None else 0 for w in weights]

        # Normalize weights to [0,1]
        norm = mcolors.Normalize(
            vmin=min(weights_clean), vmax=max(weights_clean))
        cmap = cm.get_cmap("viridis")

        # Map to colors
        colors = [
            cmap(norm(w)) if w is not None else "gray" for w in weights_clean]
        return colors

    @classmethod
    def show_undirected_graph(
        cls,
        graph,
        output_file: str,
        figsize: tuple[float, float] = (36.0, 20.0),
        default_node_sizes: int = 300,
    ):
        """
        Reads a .graphml file and displays the undirected graph.
        Parameters:
        - graph (nx.Graph): graph to be visualized, in networkx.Graph format
        - output_file (str): Path to the output graph image
        """
        if not isinstance(graph, nx.Graph):
            raise TypeError("graph must be a networkx.Graph instance")

        # Ensure graph is undirected
        if graph.is_directed():
            graph = graph.to_undirected()

        # Layout
        pos = nx.spring_layout(graph, seed=42)

        # Edge colors
        edge_colors = cls._map_edge_color(graph)

        # Node sizes
        node_sizes = [default_node_sizes] * graph.number_of_nodes()

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
            width=2,
        )
        nx.draw_networkx_labels(graph, pos, font_size=10, font_color="black")

        plt.axis("off")
        plt.tight_layout()
        plt.savefig(output_file, format="png", dpi=300)
        plt.close()

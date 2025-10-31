from __future__ import annotations

import os
from typing import Dict, List, Tuple, Optional

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize, to_hex


class GraphDisplay:
    """
    Base class that show processed graph
    """

    @classmethod
    def _map_edge_color(cls, graph: nx.Graph) -> List[str]:
        """
        Map the graph edge weight to a color.

        Parameters:
        - graph (nxGraph): networkx graph

        Return:
        - List: The list of color code
        """
        if graph.number_of_edges() == 0:
            return []

        weights = []
        for u, v in graph.edges():
            data = graph.get_edge_data(u, v, default={})
            # In case of MultiGraph choose the first edge's weight
            if isinstance(data, dict) and "weight" not in data and len(data) > 0 and 0 in data:
                data = data[0]
            weights.append(float(data.get("weight", 1.0)))

        w_min = min(weights)
        w_max = max(weights)
        if w_max == w_min:
            normed = [0.5 for _ in weights]
        else:
            norm = Normalize(vmin=w_min, vmax=w_max)
            normed = [norm(w) for w in weights]

        cmap = cm.plasma
        colors = [to_hex(cmap(v)) for v in normed]
        return colors

    @classmethod
    def show_undirected_graph(
        cls,
        graph,
        output_file: str,
        figsize: Tuple[float, float] = (36.0, 20.0),
        default_node_sizes: Optional[Dict] = None,
    ) -> None:
        """
        Reads a .graphml file and displays the undirected graph.

        Parameters:
        - graph (nx.Graph): graph to be visualized, in networkx.Graph format
        - output_file (str): Path to the output graph image
        - figsize (tuple): Matplotlib figure size
        - default_node_sizes (dict or None): Optional mapping of node -> size
        """
        if not isinstance(graph, (nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph)):
            raise TypeError(
                "graph must be a networkx Graph/DiGraph/MultiGraph/MultiDiGraph.")

        if graph.number_of_nodes() == 0:
            # Create an empty image to indicate no content
            os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
            fig, ax = plt.subplots(figsize=figsize)
            ax.axis("off")
            ax.text(0.5, 0.5, "Empty graph", ha="center",
                    va="center", fontsize=24)
            fig.savefig(output_file, bbox_inches="tight", dpi=300)
            plt.close(fig)
            return

        G = graph.to_undirected() if graph.is_directed() else graph

        pos = nx.spring_layout(G, seed=42)

        # Node sizes
        if default_node_sizes is not None:
            sizes = [float(default_node_sizes.get(n, 300.0))
                     for n in G.nodes()]
        else:
            degrees = dict(G.degree())
            if degrees:
                d_vals = list(degrees.values())
                d_min, d_max = min(d_vals), max(d_vals)
                if d_max == d_min:
                    sizes = [800.0 for _ in G.nodes()]
                else:
                    # Scale degrees to a size range
                    low, high = 300.0, 3000.0
                    sizes = [
                        low + (high - low) *
                        ((degrees[n] - d_min) / (d_max - d_min))
                        for n in G.nodes()
                    ]
            else:
                sizes = [800.0 for _ in G.nodes()]

        # Edge attributes
        edge_colors = cls._map_edge_color(G)
        # Edge widths based on weight
        weights = []
        for u, v in G.edges():
            data = G.get_edge_data(u, v, default={})
            if isinstance(data, dict) and "weight" not in data and len(data) > 0 and 0 in data:
                data = data[0]
            weights.append(float(data.get("weight", 1.0)))

        if weights:
            w_min, w_max = min(weights), max(weights)
            if w_max == w_min:
                widths = [2.0 for _ in weights]
            else:
                low_w, high_w = 0.5, 6.0
                widths = [
                    low_w + (high_w - low_w) * ((w - w_min) / (w_max - w_min)) for w in weights]
        else:
            widths = []

        os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
        fig, ax = plt.subplots(figsize=figsize)
        ax.axis("off")

        nx.draw_networkx_nodes(
            G,
            pos=pos,
            node_size=sizes,
            node_color="#3871c1",
            alpha=0.9,
            ax=ax,
        )
        nx.draw_networkx_edges(
            G,
            pos=pos,
            edge_color=edge_colors if edge_colors else "#999999",
            width=widths if widths else 1.5,
            alpha=0.8,
            ax=ax,
        )
        labels = {n: str(G.nodes[n].get("label", n)) for n in G.nodes()}
        nx.draw_networkx_labels(G, pos=pos, labels=labels,
                                font_size=10, font_color="#111111", ax=ax)

        # Optional colorbar for edges if there is a range of weights
        if weights and (max(weights) != min(weights)):
            norm = Normalize(vmin=min(weights), vmax=max(weights))
            sm = cm.ScalarMappable(norm=norm, cmap=cm.plasma)
            sm.set_array([])
            cbar = fig.colorbar(sm, ax=ax, fraction=0.03, pad=0.02)
            cbar.set_label("Edge Weight", rotation=90)

        fig.savefig(output_file, bbox_inches="tight", dpi=300)
        plt.close(fig)

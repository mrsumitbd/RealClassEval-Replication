import os
from pathlib import Path
from typing import List, Tuple, Union

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx


class GraphDisplay:
    '''
    Base class that show processed graph
    '''
    @classmethod
    def _map_edge_color(cls, graph: nx.Graph) -> List[str]:
        '''
        Map the graph edge weight to a color.
        Parameters:
        - graph (nxGraph): networkx graph
        Return:
        - List: The list of color code
        '''
        edges = list(graph.edges(data=True))
        if not edges:
            return []

        weights = [float(attr.get("weight", 1.0)) for _, _, attr in edges]
        wmin = min(weights)
        wmax = max(weights)

        if wmin == wmax:
            return [mpl.colors.to_hex(mpl.cm.viridis(0.5)) for _ in weights]

        norm = mpl.colors.Normalize(vmin=wmin, vmax=wmax)
        cmap = mpl.cm.viridis
        return [mpl.colors.to_hex(cmap(norm(w))) for w in weights]

    @classmethod
    def show_undirected_graph(
        cls,
        graph: Union[str, nx.Graph],
        output_file: str,
        figsize: Tuple[float, float] = (36.0, 20.0),
        default_node_size: int = 300,
    ) -> None:
        '''
        Reads a graph source and displays the undirected graph, saving it as an image.
        Parameters:
        - graph (str|nx.Graph): graph to be visualized, either a path to a graph file or a networkx.Graph
        - output_file (str): Path to the output graph image
        '''
        # Load graph if a path is provided
        if isinstance(graph, str):
            path = Path(graph)
            if not path.exists():
                raise FileNotFoundError(f"Graph file not found: {graph}")
            suffix = path.suffix.lower()
            if suffix == ".graphml":
                G = nx.read_graphml(path)
            elif suffix == ".gexf":
                G = nx.read_gexf(path)
            elif suffix in {".gml"}:
                G = nx.read_gml(path)
            elif suffix in {".gpickle", ".pkl"}:
                G = nx.read_gpickle(path)
            else:
                raise ValueError(f"Unsupported graph format: {suffix}")
        elif isinstance(graph, nx.Graph):
            G = graph
        else:
            raise TypeError("graph must be a file path or a networkx.Graph")

        if G.is_directed():
            G = G.to_undirected()

        if len(G) == 0:
            # Create an empty figure to save
            plt.figure(figsize=figsize)
            plt.axis("off")
            plt.savefig(output_file, bbox_inches="tight", dpi=300)
            plt.close()
            return

        # Layout
        pos = nx.spring_layout(G, seed=42)

        # Node sizes
        node_sizes = []
        for n, data in G.nodes(data=True):
            node_sizes.append(int(data.get("size", default_node_size)))

        # Node colors mapped by node 'weight' if present, else default
        node_weights = [float(data.get("weight", None))
                        for _, data in G.nodes(data=True)]
        if any(w is not None for w in node_weights):
            # Replace None with median of existing weights
            existing = [w for w in node_weights if w is not None]
            if existing:
                median_w = sorted(existing)[len(existing) // 2]
            else:
                median_w = 1.0
            node_weights = [median_w if w is None else w for w in node_weights]
            nmin, nmax = min(node_weights), max(node_weights)
            if nmin == nmax:
                node_colors = [mpl.colors.to_hex(
                    mpl.cm.plasma(0.5)) for _ in node_weights]
            else:
                n_norm = mpl.colors.Normalize(vmin=nmin, vmax=nmax)
                n_cmap = mpl.cm.plasma
                node_colors = [mpl.colors.to_hex(
                    n_cmap(n_norm(w))) for w in node_weights]
        else:
            node_colors = ["#87ceeb"] * G.number_of_nodes()  # skyblue default

        # Edge colors and widths
        edge_colors = cls._map_edge_color(G)
        if edge_colors and len(edge_colors) != G.number_of_edges():
            edge_colors = ["#999999"] * G.number_of_edges()
        edge_weights = [float(attr.get("weight", 1.0))
                        for _, _, attr in G.edges(data=True)]
        edge_widths = [max(0.5, 0.5 + 1.5 * w)
                       for w in edge_weights] if edge_weights else []

        # Draw
        plt.figure(figsize=figsize)
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes,
                               node_color=node_colors, linewidths=0.5, edgecolors="#333333")
        if G.number_of_edges() > 0:
            nx.draw_networkx_edges(
                G, pos, edge_color=edge_colors if edge_colors else "#999999", width=edge_widths)
        nx.draw_networkx_labels(G, pos, font_size=10)

        plt.axis("off")
        plt.tight_layout()

        out_dir = os.path.dirname(os.path.abspath(output_file))
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        plt.savefig(output_file, bbox_inches="tight", dpi=300)
        plt.close()

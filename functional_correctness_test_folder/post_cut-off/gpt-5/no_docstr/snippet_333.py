import math
from pathlib import Path
from typing import Any, Optional

import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class GraphDisplay:

    @classmethod
    def _map_edge_color(cls, graph: nx.Graph) -> list[str]:
        colors: list[str] = []
        if graph.number_of_edges() == 0:
            return colors

        # If explicit edge colors exist, use them
        has_explicit_color = any(
            ("color" in data and data["color"] is not None) for _, _, data in graph.edges(data=True)
        )
        if has_explicit_color:
            for _, _, data in graph.edges(data=True):
                c = data.get("color", "#888888")
                try:
                    # normalize various color formats
                    c_mapped = mcolors.to_hex(c)
                except Exception:
                    c_mapped = "#888888"
                colors.append(c_mapped)
            return colors

        # Map weights to a colormap if available
        weights = []
        has_weight = False
        for _, _, data in graph.edges(data=True):
            if "weight" in data and data["weight"] is not None:
                try:
                    w = float(data["weight"])
                    has_weight = True
                except Exception:
                    w = 1.0
                weights.append(w)
            else:
                weights.append(1.0)

        if has_weight:
            w_arr = np.array(weights, dtype=float)
            if np.all(np.isfinite(w_arr)):
                # Normalize robustly using percentiles to reduce outlier impact
                lo = np.percentile(w_arr, 5) if w_arr.size > 1 else w_arr.min()
                hi = np.percentile(
                    w_arr, 95) if w_arr.size > 1 else w_arr.max()
                if math.isclose(hi, lo):
                    hi = lo + 1.0
                norm = mcolors.Normalize(vmin=lo, vmax=hi, clip=True)
                cmap = cm.get_cmap("viridis")
                for w in w_arr:
                    colors.append(mcolors.to_hex(cmap(norm(w))))
                return colors

        # Fallback flat color
        colors = ["#888888"] * graph.number_of_edges()
        return colors

    @classmethod
    def show_undirected_graph(
        cls,
        graph: nx.Graph,
        output_file: str,
        figsize: tuple[float, float] = (36.0, 20.0),
        default_node_sizes: Optional[dict[Any, float] | float] = None,
    ) -> str:
        # Positions
        if graph.number_of_nodes() > 0:
            pos = nx.spring_layout(graph, seed=42)
        else:
            pos = {}

        # Node colors
        node_colors: list[str] = []
        for n, data in graph.nodes(data=True):
            c = data.get("color", "skyblue")
            try:
                node_colors.append(mcolors.to_hex(c))
            except Exception:
                node_colors.append("skyblue")

        # Node sizes
        sizes: list[float] = []
        numeric_default: Optional[float] = None
        mapping_default: Optional[dict[Any, float]] = None
        if isinstance(default_node_sizes, (int, float)):
            numeric_default = float(default_node_sizes)
        elif isinstance(default_node_sizes, dict):
            mapping_default = default_node_sizes

        for n, data in graph.nodes(data=True):
            if "size" in data:
                try:
                    sizes.append(float(data["size"]))
                    continue
                except Exception:
                    pass
            if mapping_default is not None and "type" in data and data["type"] in mapping_default:
                try:
                    sizes.append(float(mapping_default[data["type"]]))
                    continue
                except Exception:
                    pass
            if numeric_default is not None:
                sizes.append(numeric_default)
            else:
                # Degree-based fallback with bounds
                deg = graph.degree[n] if graph.number_of_nodes() > 0 else 0
                sizes.append(300.0 + 50.0 * float(deg))

        # Edge colors and widths
        edge_colors = cls._map_edge_color(graph)
        widths: list[float] = []
        if graph.number_of_edges() > 0:
            weights = []
            has_weight = False
            for _, _, data in graph.edges(data=True):
                w = data.get("weight", 1.0)
                try:
                    w = float(w)
                    has_weight = has_weight or ("weight" in data)
                except Exception:
                    w = 1.0
                weights.append(w)
            w_arr = np.array(weights, dtype=float)
            if w_arr.size > 0 and np.all(np.isfinite(w_arr)):
                lo = np.percentile(
                    w_arr, 10) if w_arr.size > 1 else w_arr.min()
                hi = np.percentile(
                    w_arr, 90) if w_arr.size > 1 else w_arr.max()
                if math.isclose(hi, lo):
                    hi = lo + 1.0
                norm = mcolors.Normalize(vmin=lo, vmax=hi, clip=True)
                for w in w_arr:
                    widths.append(0.5 + 5.5 * float(norm(w)))
            else:
                widths = [1.5] * graph.number_of_edges()
        else:
            widths = []

        # Draw
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_axis_off()

        if graph.number_of_nodes() > 0:
            nx.draw_networkx_nodes(
                graph,
                pos,
                node_color=node_colors if len(
                    node_colors) == graph.number_of_nodes() else "skyblue",
                node_size=sizes if len(
                    sizes) == graph.number_of_nodes() else 300.0,
                linewidths=0.5,
                edgecolors="#333333",
                ax=ax,
            )

        if graph.number_of_edges() > 0:
            nx.draw_networkx_edges(
                graph,
                pos,
                edge_color=edge_colors if len(
                    edge_colors) == graph.number_of_edges() else "#888888",
                width=widths if len(
                    widths) == graph.number_of_edges() else 1.5,
                alpha=0.9,
                ax=ax,
            )

        # Labels
        if graph.number_of_nodes() <= 200:
            try:
                nx.draw_networkx_labels(
                    graph, pos, font_size=8, font_color="#111111", ax=ax)
            except Exception:
                pass

        # Save
        out_path = Path(output_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        plt.tight_layout()
        fig.savefig(out_path.as_posix(), dpi=150,
                    bbox_inches="tight", facecolor="white")
        plt.close(fig)
        return out_path.as_posix()

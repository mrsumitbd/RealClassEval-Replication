from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Iterable

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import cm, colors


class GraphDisplay:
    '''
    Base class that show processed graph
    '''
    @classmethod
    def _map_edge_color(cls, graph: nx.Graph) -> list[str]:
        '''
        Map the graph edge weight to a color.
        Parameters:
        - graph (nxGraph): networkx graph
        Return:
        - List: The list of color code
        '''
        edge_weights: list[float] = []
        for _, _, data in graph.edges(data=True):
            w = data.get('weight', 1.0)
            try:
                w = float(w)
            except Exception:
                w = 1.0
            edge_weights.append(w)

        if not edge_weights:
            return []

        w_min, w_max = min(edge_weights), max(edge_weights)
        if w_min == w_max:
            return ['#6a3d9a'] * len(edge_weights)

        norm = colors.Normalize(vmin=w_min, vmax=w_max)
        cmap = cm.plasma
        return [colors.to_hex(cmap(norm(w))) for w in edge_weights]

    @classmethod
    def show_undirected_graph(
        cls,
        graph: nx.Graph | str | Path,
        output_file: str,
        figsize: tuple[float, float] = (36.0, 20.0),
        default_node_sizes: int | Mapping[Any, float] | None = None,
    ) -> None:
        '''
        Reads a .graphml file and displays the undirected graph.
        Parameters:
        - graph (str|Path|nx.Graph): graph to be visualized, or a path to a .graphml file
        - output_file (str): Path to the output graph image
        '''
        # Load graph if a path is provided
        if isinstance(graph, (str, Path)):
            path = Path(graph)
            if not path.exists():
                raise FileNotFoundError(f'Graph file not found: {path}')
            if path.suffix.lower() == '.graphml':
                G_loaded = nx.read_graphml(path)
            else:
                raise ValueError(
                    f'Unsupported graph format: {path.suffix}. Expected .graphml')
            G = nx.Graph(G_loaded)
        elif isinstance(graph, nx.Graph):
            G = nx.Graph(graph)
        else:
            raise TypeError(
                'graph must be a networkx.Graph or a path to a .graphml file')

        if G.number_of_nodes() == 0:
            raise ValueError('Graph has no nodes to display')
        if default_node_sizes is None:
            default_node_sizes = 600

        # Layout
        seed = 42
        if G.number_of_nodes() <= 200:
            pos = nx.kamada_kawai_layout(G)
        else:
            pos = nx.spring_layout(G, seed=seed)

        # Node sizes (prefer explicit "size", fallback to normalized "weight", else default)
        nodes = list(G.nodes())
        explicit_sizes: list[float] = []
        has_explicit_size = any(('size' in G.nodes[n]) for n in nodes)
        if has_explicit_size:
            for n in nodes:
                val = G.nodes[n].get('size', None)
                try:
                    explicit_sizes.append(float(val) if val is not None else float(
                        default_node_sizes))  # type: ignore[arg-type]
                except Exception:
                    # type: ignore[arg-type]
                    explicit_sizes.append(float(default_node_sizes))
            node_sizes = explicit_sizes
        else:
            weights = []
            has_weight = any(('weight' in G.nodes[n]) for n in nodes)
            if has_weight:
                for n in nodes:
                    try:
                        weights.append(float(G.nodes[n].get('weight', 1.0)))
                    except Exception:
                        weights.append(1.0)
                w_min, w_max = min(weights), max(weights)
                if w_min == w_max:
                    # type: ignore[arg-type]
                    node_sizes = [float(default_node_sizes)] * len(nodes)
                else:
                    # Scale sizes to [0.6, 1.8] * default
                    node_sizes = [
                        # type: ignore[arg-type]
                        float(default_node_sizes) *
                        (0.6 + 1.2 * (w - w_min) / (w_max - w_min))
                        for w in weights
                    ]
            else:
                node_sizes = [float(default_node_sizes)] * \
                    len(nodes)  # type: ignore[arg-type]

            # Allow mapping override if dict passed
            if isinstance(default_node_sizes, Mapping):
                node_sizes = [float(default_node_sizes.get(
                    n, node_sizes[i])) for i, n in enumerate(nodes)]

        # Node colors (based on weight if present)
        has_node_weight = any(('weight' in G.nodes[n]) for n in nodes)
        if has_node_weight:
            vals = []
            for n in nodes:
                try:
                    vals.append(float(G.nodes[n].get('weight', 1.0)))
                except Exception:
                    vals.append(1.0)
            vmin, vmax = min(vals), max(vals)
            if vmin == vmax:
                node_colors = ['#1f78b4'] * len(nodes)
            else:
                norm_nodes = colors.Normalize(vmin=vmin, vmax=vmax)
                cmap_nodes = cm.viridis
                node_colors = [colors.to_hex(
                    cmap_nodes(norm_nodes(v))) for v in vals]
        else:
            node_colors = ['#1f78b4'] * len(nodes)

        # Edge properties
        edgelist = list(G.edges())
        edge_colors = cls._map_edge_color(G)
        # Edge widths (based on weight)
        edge_weights = []
        for u, v in edgelist:
            data = G.get_edge_data(u, v, default={})
            w = data.get('weight', 1.0)
            try:
                w = float(w)
            except Exception:
                w = 1.0
            edge_weights.append(w)
        if edge_weights:
            ew_min, ew_max = min(edge_weights), max(edge_weights)
            if ew_min == ew_max:
                edge_widths = [1.5] * len(edge_weights)
            else:
                edge_widths = [
                    0.5 + 3.0 * (w - ew_min) / (ew_max - ew_min) for w in edge_weights]
        else:
            edge_widths = []

        # Labels
        labels = {n: str(G.nodes[n].get('label', n)) for n in nodes}

        # Draw
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_axis_off()

        nx.draw_networkx_nodes(
            G,
            pos,
            node_size=node_sizes,
            node_color=node_colors,
            linewidths=0.5,
            edgecolors='#333333',
            ax=ax,
        )
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=edgelist,
            edge_color=edge_colors if edge_colors else '#999999',
            width=edge_widths if edge_widths else 1.5,
            alpha=0.85,
            ax=ax,
        )
        nx.draw_networkx_labels(
            G,
            pos,
            labels=labels,
            font_size=10,
            font_color='#111111',
            ax=ax,
        )

        title = G.graph.get('name') or 'Undirected Graph'
        ax.set_title(title, fontsize=16)
        plt.tight_layout()

        out_path = Path(output_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, bbox_inches='tight', dpi=200)
        plt.close(fig)

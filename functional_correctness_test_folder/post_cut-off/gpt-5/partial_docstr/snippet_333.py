import os
from typing import Union, Tuple, Any
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib import cm


class GraphDisplay:
    '''
    Base class that show processed graph
    '''
    @classmethod
    def _map_edge_color(cls, graph: nx.Graph):
        # If edges have an explicit 'color' attribute, use it directly
        colors = []
        has_explicit_color = any(
            'color' in data for _, _, data in graph.edges(data=True))
        if has_explicit_color:
            for u, v, data in graph.edges(data=True):
                colors.append(data.get('color', 'gray'))
            return colors

        # If edges have 'weight', map to a colormap; otherwise default to gray
        weights = [data.get('weight') for _, _, data in graph.edges(data=True)]
        if any(w is not None for w in weights) and len(weights) > 0:
            # Replace None with 0 for normalization purposes
            clean_weights = [0.0 if w is None else float(w) for w in weights]
            vmin, vmax = min(clean_weights), max(clean_weights)
            # Avoid zero range normalization
            if vmin == vmax:
                vmin = vmin - 1.0
                vmax = vmax + 1.0
            norm = Normalize(vmin=vmin, vmax=vmax)
            cmap = cm.get_cmap('viridis')
            colors = [cmap(norm(w)) for w in clean_weights]
            return colors

        # Fallback to uniform gray color
        return ['gray'] * graph.number_of_edges()

    @classmethod
    def show_undirected_graph(
        cls,
        graph: Any,
        output_file: str,
        figsize: Tuple[float, float] = (36.0, 20.0),
        default_node_sizes: Union[int, float] = 300
    ):
        '''
        Reads a .graphml file and displays the undirected graph.
        Parameters:
        - graph (nx.Graph): graph to be visualized, in networkx.Graph format
        - output_file (str): Path to the output graph image
        '''
        if not isinstance(graph, (nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph)):
            raise TypeError("graph must be a networkx graph instance")

        # Ensure undirected view for visualization
        if isinstance(graph, (nx.DiGraph, nx.MultiDiGraph)):
            G = graph.to_undirected()
        else:
            G = graph

        # Layout
        pos = nx.spring_layout(G, seed=42)

        # Node attributes
        node_sizes = []
        node_colors = []
        has_size_attr = any('size' in G.nodes[n] for n in G.nodes)
        has_color_attr = any('color' in G.nodes[n] for n in G.nodes)
        for n in G.nodes:
            node_sizes.append(G.nodes[n].get(
                'size', default_node_sizes) if has_size_attr else default_node_sizes)
            node_colors.append(G.nodes[n].get(
                'color', 'skyblue') if has_color_attr else 'skyblue')

        # Edge visual attributes
        edge_colors = cls._map_edge_color(G)

        # Edge widths (optional: map from weight)
        edge_weights = [data.get('weight')
                        for _, _, data in G.edges(data=True)]
        if any(w is not None for w in edge_weights):
            clean_weights = [0.0 if w is None else float(
                w) for w in edge_weights]
            # Scale widths to a reasonable range
            wmin, wmax = min(clean_weights), max(clean_weights)
            if wmin == wmax:
                widths = [2.0 for _ in clean_weights]
            else:
                # Linear scaling between 0.5 and 6.0
                widths = [0.5 + 5.5 * ((w - wmin) / (wmax - wmin))
                          for w in clean_weights]
        else:
            widths = [1.5] * G.number_of_edges()

        # Prepare output directory
        os.makedirs(os.path.dirname(
            os.path.abspath(output_file)), exist_ok=True)

        # Plot
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_axis_off()

        nx.draw_networkx_nodes(
            G, pos,
            node_size=node_sizes,
            node_color=node_colors,
            linewidths=0.5,
            edgecolors='k',
            ax=ax
        )

        nx.draw_networkx_edges(
            G, pos,
            width=widths,
            edge_color=edge_colors,
            alpha=0.8,
            ax=ax
        )

        # Labels if present
        has_label_attr = any('label' in G.nodes[n] for n in G.nodes)
        labels = {n: (G.nodes[n].get('label', str(n))
                      if has_label_attr else str(n)) for n in G.nodes}
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, ax=ax)

        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close(fig)

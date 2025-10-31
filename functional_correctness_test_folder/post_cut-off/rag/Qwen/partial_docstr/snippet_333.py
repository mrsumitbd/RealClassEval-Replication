
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class GraphDisplay:
    '''
    Base class that show processed graph
    '''
    @classmethod
    def _map_edge_color(cls, graph: nx.Graph):
        '''
        Map the graphnode weight to a color.
        Parameters:
        - graph (nx.Graph): networkx graph
        Return:
        - List: The list of color code
        '''
        weights = nx.get_edge_attributes(graph, 'weight')
        if not weights:
            return ['black'] * len(graph.edges())
        max_weight = max(weights.values())
        min_weight = min(weights.values())
        norm = mcolors.Normalize(vmin=min_weight, vmax=max_weight)
        cmap = plt.cm.get_cmap('coolwarm')
        return [cmap(norm(weight)) for weight in weights.values()]

    @classmethod
    def show_undirected_graph(cls, graph, output_file: str, figsize: tuple[float, float] = (36.0, 20.0)):
        '''
        Reads a .graphml file and displays the undirected graph.
        Parameters:
        - graph (nx.Graph): graph to be visualized, in networkx.Graph format
        - output_file (str): Path to the output graph image
        '''
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(graph, seed=42)
        edge_colors = cls._map_edge_color(graph)
        nx.draw(graph, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=10, font_weight='bold',
                edge_color=edge_colors, width=2.0, arrows=False)
        sm = plt.cm.ScalarMappable(cmap=plt.cm.coolwarm, norm=mcolors.Normalize(vmin=min(nx.get_edge_attributes(graph, 'weight').values(), default=0),
                                                                                vmax=max(nx.get_edge_attributes(graph, 'weight').values(), default=1)))
        sm.set_array([])
        plt.colorbar(sm, label='Edge Weight')
        plt.title('Undirected Graph Visualization')
        plt.savefig(output_file, format='png')
        plt.close()
